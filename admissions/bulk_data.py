"""Validated Excel/CSV catalogue and lead import/export helpers."""
import csv
import io
import json
import re
import zipfile
from pathlib import PurePosixPath

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.db import transaction
from openpyxl import Workbook, load_workbook
from PIL import Image

from .models import BulkDataBatch, College, CollegeImage, Course, Lead, OnlineCourse


DATASETS = {
    "leads": {
        "title": "Leads", "headers": ["Student Name", "Father Name", "Mobile Number", "Email", "City", "Course", "Preferred College", "10th Percentage", "12th Percentage", "Entrance Rank", "Source", "Status", "Call Outcome", "Assigned Username", "Consent"],
        "sample": ["Aarav Sharma", "Raj Sharma", "9876543210", "student@example.com", "New Delhi", "B.Tech CSE", "Example College", "82.50", "86.20", "JEE 75000", "Website", "New Enquiry", "Untouched", "", "Yes"],
    },
    "courses": {
        "title": "Courses", "headers": ["Course Name", "Category", "Level", "Duration", "Specialization", "Eligibility", "Entrance Exam", "Annual Fee", "Total Fee", "Seats", "Short Description", "Career Path", "Motivation", "Brochure URL", "SEO Title", "SEO Description", "SEO Keywords", "SEO Slug", "Image Filename", "External Image URL", "Image Source URL"],
        "sample": ["B.Tech CSE", "Engineering", "UG", "4 Years", "Computer Science", "10+2 with PCM", "JEE Main", "150000", "600000", "120", "Computer science degree", "Software, AI and technology careers", "Build the future with technology", "", "B.Tech CSE Admission", "Fees, eligibility and admission details", "btech-cse.jpg", "", ""],
    },
    "colleges": {
        "title": "Colleges", "headers": ["College Name", "University", "University Group", "College Type", "City", "State", "Address", "Website", "Phone", "Email", "Courses", "Short Description", "Career Path", "Motivation", "Approvals", "Ranking", "Accreditation", "Average Package", "Highest Package", "Hostel", "Admission Deadline", "Scholarship", "Admission Mode", "Brochure URL", "SEO Title", "SEO Description", "SEO Keywords", "SEO Slug", "Image Filename", "Gallery Image Filenames", "External Image URL", "Image Source URL", "Featured", "Active"],
        "sample": ["Example Institute", "GGSIPU", "IPU", "Engineering", "New Delhi", "Delhi", "Campus address", "https://example.edu", "01100000000", "info@example.edu", "B.Tech CSE, BBA", "Top college for professional education", "College description", "Build your career with strong academics and placements", "AICTE", "NIRF details", "NAAC A+", "8 LPA", "25 LPA", "Boys & Girls", "30 June 2027", "Merit scholarship available", "Counselling / MQ", "", "Example Institute Admission", "Courses, fees, placement and admission", "example-campus.jpg", "gallery1.jpg, gallery2.jpg", "", "", "No", "Yes"],
    },
    "medical_colleges": {
        "title": "Medical Colleges", "headers": ["College Name", "University", "University Group", "City", "State", "Address", "Website", "Phone", "Email", "Courses", "Short Description", "Career Path", "Motivation", "Approvals", "Ranking", "Accreditation", "Average Package", "Highest Package", "Hostel", "Admission Deadline", "Scholarship", "Admission Mode", "Brochure URL", "SEO Title", "SEO Description", "SEO Keywords", "SEO Slug", "Image Filename", "Gallery Image Filenames", "External Image URL", "Image Source URL", "Featured", "Active"],
        "sample": ["Example Medical College", "Example University", "OTHER", "New Delhi", "Delhi", "Campus address", "https://example.edu", "01100000000", "info@example.edu", "MBBS, BDS", "Medical education with clinical exposure", "Medical college description", "Start your journey toward a healthcare career", "NMC", "Ranking details", "NAAC A+", "", "", "Boys & Girls", "30 June 2027", "Merit scholarship", "NEET counselling", "", "Medical College Admission", "Fees, courses and admission details", "medical-campus.jpg", "medical-gallery.jpg", "", "", "No", "Yes"],
    },
    "online_courses": {
        "title": "Online Courses", "headers": ["Title", "Category", "Provider", "Specialization", "Short Description", "Career Path", "Motivation", "Duration", "Fee", "Eligibility", "Accreditation", "Exam Mode", "LMS Details", "Course URL", "Application URL", "Brochure URL", "SEO Title", "SEO Description", "SEO Keywords", "SEO Slug", "Image Filename", "External Image URL", "Image Source URL", "Featured", "Active"],
        "sample": ["Online BBA", "Management", "Example University", "General", "Flexible online learning", "Flexible online degree", "Study from anywhere and grow your career", "3 Years", "₹25,000/Semester", "10+2", "UGC entitled", "Online proctored", "Recorded and live classes", "https://example.com/course", "https://example.com/apply", "", "Online BBA Admission", "Fees, eligibility and online learning details", "online-bba.jpg", "", "", "Yes", "Yes"],
    },
}


def read_rows(upload):
    if upload.name.lower().endswith(".csv"):
        rows = list(csv.DictReader(io.StringIO(upload.read().decode("utf-8-sig"))))
    else:
        sheet = load_workbook(upload, read_only=True, data_only=True).active
        values = list(sheet.iter_rows(values_only=True))
        if not values: return []
        headers = [str(value or "").strip() for value in values[0]]
        rows = [dict(zip(headers, row)) for row in values[1:]]
    return [row for row in rows if any(value not in (None, "") for value in row.values())]


def read_image_zip(upload):
    if not upload: return {}
    images, total_size = {}, 0
    try:
        archive = zipfile.ZipFile(upload)
    except zipfile.BadZipFile as exc:
        raise ValidationError("Images ZIP is invalid or damaged") from exc
    files = [item for item in archive.infolist() if not item.is_dir() and not PurePosixPath(item.filename).name.startswith(".")]
    if len(files) > 1000: raise ValidationError("Images ZIP cannot contain more than 1,000 files")
    for item in files:
        filename = PurePosixPath(item.filename).name
        extension = PurePosixPath(filename).suffix.lower()
        if extension not in {".jpg", ".jpeg", ".png", ".webp"}: raise ValidationError(f"Unsupported image type in ZIP: {filename}")
        if item.flag_bits & 0x1: raise ValidationError("Password-protected ZIP files are not supported")
        if item.file_size > 5 * 1024 * 1024: raise ValidationError(f"Image exceeds 5 MB: {filename}")
        total_size += item.file_size
        if total_size > 200 * 1024 * 1024: raise ValidationError("Uncompressed images cannot exceed 200 MB")
        key = filename.casefold()
        if key in images: raise ValidationError(f"Duplicate image filename in ZIP: {filename}")
        data = archive.read(item)
        try:
            with Image.open(io.BytesIO(data)) as image: image.verify()
        except Exception as exc:
            raise ValidationError(f"Invalid image file: {filename}") from exc
        images[key] = (filename, data)
    return images


def value(row, name):
    lowered = {str(key).strip().lower(): val for key, val in row.items()}
    result = lowered.get(name.lower(), "")
    return str(result).strip() if result is not None else ""


def as_bool(raw, default=False):
    if raw == "": return default
    lowered = raw.strip().lower()
    if lowered in {"yes", "true", "1", "active", "y"}: return True
    if lowered in {"no", "false", "0", "inactive", "n"}: return False
    raise ValidationError(f"'{raw}' must be Yes or No")


def valid_choice(raw, choices, field, default):
    if not raw: return default
    lookup = {str(key).lower(): key for key, _ in choices}
    if raw.lower() not in lookup: raise ValidationError(f"Invalid {field}: {raw}")
    return lookup[raw.lower()]


def save_object(obj, values):
    for field, val in values.items():
        setattr(obj, field, val)
    obj.full_clean()
    obj.save()


def split_courses(raw):
    return [name.strip() for name in re.split(r"[,;|]", raw) if name.strip()]


def matching_key(dataset, row):
    if dataset == "leads": return re.sub(r"\D", "", value(row, "Mobile Number"))[-10:]
    if dataset == "courses": return value(row, "Course Name")
    if dataset == "colleges": return f'{value(row, "College Name")}|{value(row, "University")}'
    if dataset == "medical_colleges": return f'{value(row, "College Name")}|{value(row, "State") or "Delhi"}'
    return value(row, "Title")


def attach_image(obj, field_name, requested_filename, images):
    if not requested_filename: return 0
    safe_name = PurePosixPath(requested_filename).name
    item = images.get(safe_name.casefold())
    if not item: raise ValidationError(f"Image not found in ZIP: {safe_name}")
    original_name, data = item
    getattr(obj, field_name).save(original_name, ContentFile(data), save=True)
    return 1


def validate_image_references(filenames, images):
    for requested in filenames:
        if requested and PurePosixPath(requested).name.casefold() not in images:
            raise ValidationError(f"Image not found in ZIP: {PurePosixPath(requested).name}")


def process_bulk_rows(dataset, rows, file_name, user, mode="upsert", images=None):
    if dataset not in DATASETS: raise ValueError("Unknown dataset")
    batch = BulkDataBatch.objects.create(dataset=dataset, mode=mode, file_name=file_name, uploaded_by=user, total_rows=len(rows))
    errors, seen, images = [], set(), images or {}
    for number, row in enumerate(rows, start=2):
        key = ""
        try:
            key = matching_key(dataset, row)
            normalized = key.casefold()
            if normalized in seen: raise ValidationError("Duplicate matching key inside uploaded file")
            with transaction.atomic():
                action, key, image_count = process_row(dataset, row, mode, user, images)
                seen.add(normalized)
                if action == "created": batch.created_count += 1
                elif action == "updated": batch.updated_count += 1
                else: batch.skipped_count += 1
                batch.imported_image_count += image_count
        except (ValidationError, ValueError) as exc:
            batch.rejected_count += 1
            detail = exc.messages if isinstance(exc, ValidationError) else [str(exc)]
            errors.append({"row": number, "key": key, "error": "; ".join(detail)})
    batch.error_report = json.dumps(errors, ensure_ascii=False)
    batch.save()
    return batch


def process_row(dataset, row, mode, user, images=None):
    images = images or {}
    if dataset == "leads":
        name, phone = value(row, "Student Name"), re.sub(r"\D", "", value(row, "Mobile Number"))[-10:]
        key = phone
        if not name or len(phone) != 10: raise ValidationError("Student Name and a valid 10-digit Mobile Number are required")
        course_name, college_name = value(row, "Course"), value(row, "Preferred College")
        course = Course.objects.filter(name__iexact=course_name).first() if course_name else None
        college = College.objects.filter(name__iexact=college_name).first() if college_name else None
        if course_name and not course: raise ValidationError(f"Course not found: {course_name}")
        if college_name and not college: raise ValidationError(f"College not found: {college_name}")
        username = value(row, "Assigned Username")
        assignee = User.objects.filter(username__iexact=username, is_active=True).first() if username else None
        if username and not assignee: raise ValidationError(f"Active user not found: {username}")
        existing = Lead.objects.filter(phone=phone).first()
        if existing and mode == "create": return "skipped", key, 0
        obj = existing or Lead(phone=phone, uploaded_by=user)
        values = {"name": name, "father_name": value(row, "Father Name"), "email": value(row, "Email"), "city": value(row, "City"), "course": course, "preferred_college": college,
                  "class_10_percentage": value(row, "10th Percentage") or None, "class_12_percentage": value(row, "12th Percentage") or None, "score": value(row, "Entrance Rank"),
                  "source": valid_choice(value(row, "Source"), Lead.SOURCE, "source", "Website"), "status": valid_choice(value(row, "Status"), Lead.STATUS, "status", "New Enquiry"),
                  "call_outcome": valid_choice(value(row, "Call Outcome"), Lead.CALL_OUTCOMES, "call outcome", "Untouched"), "assigned_to": assignee,
                  "consent": as_bool(value(row, "Consent"), False)}
        save_object(obj, values)
        return ("updated" if existing else "created"), key, 0

    if dataset == "courses":
        name = value(row, "Course Name"); key = name
        if not name: raise ValidationError("Course Name is required")
        existing = Course.objects.filter(name__iexact=name).first()
        if existing and mode == "create": return "skipped", key, 0
        obj = existing or Course(name=name)
        save_object(obj, {"name": name, "category": valid_choice(value(row, "Category"), Course.CATEGORIES, "category", "Other"),
            "level": valid_choice(value(row, "Level"), Course._meta.get_field("level").choices, "level", "UG"), "duration": value(row, "Duration"),
            "specialization": value(row, "Specialization"), "eligibility": value(row, "Eligibility"), "entrance_exam": value(row, "Entrance Exam"),
            "annual_fee": value(row, "Annual Fee"), "total_fee": value(row, "Total Fee"), "seats": int(float(value(row, "Seats"))) if value(row, "Seats") else None,
            "short_description": value(row, "Short Description"), "career_description": value(row, "Career Path") or value(row, "Description") or value(row, "Career Description"), "motivation": value(row, "Motivation"),
            "brochure_url": value(row, "Brochure URL"), "seo_title": value(row, "SEO Title"), "seo_description": value(row, "SEO Description"), "seo_keywords": value(row, "SEO Keywords"), "seo_slug": value(row, "SEO Slug"),
            "external_image_url": value(row, "External Image URL"), "image_source_url": value(row, "Image Source URL")})
        validate_image_references([value(row, "Image Filename")], images)
        image_count = attach_image(obj, "image", value(row, "Image Filename"), images)
        return ("updated" if existing else "created"), key, image_count

    if dataset in {"colleges", "medical_colleges"}:
        name, university, state = value(row, "College Name"), value(row, "University"), value(row, "State") or "Delhi"
        key = f"{name}|{state if dataset == 'medical_colleges' else university}"
        if not name or not university: raise ValidationError("College Name and University are required")
        existing = (College.objects.filter(name__iexact=name, state__iexact=state).first() if dataset == "medical_colleges" else College.objects.filter(name__iexact=name, university__iexact=university).first())
        if existing and mode == "create": return "skipped", key, 0
        obj = existing or College(name=name, university=university)
        group = valid_choice(value(row, "University Group"), College.GROUPS, "university group", "OTHER")
        college_type = "Medical" if dataset == "medical_colleges" else valid_choice(value(row, "College Type"), College.TYPES, "college type", "General")
        save_object(obj, {"name": name, "university": university, "university_group": group, "college_type": college_type, "city": value(row, "City") or "New Delhi", "state": state,
            "short_description": value(row, "Short Description"), "description": value(row, "Career Path") or value(row, "Description"), "motivation": value(row, "Motivation"), "address": value(row, "Address"), "website": value(row, "Website"), "phone": value(row, "Phone"), "email": value(row, "Email"),
            "approvals": value(row, "Approvals"), "ranking": value(row, "Ranking"), "accreditation": value(row, "Accreditation"), "average_package": value(row, "Average Package"), "highest_package": value(row, "Highest Package"), "hostel": value(row, "Hostel"),
            "admission_deadline": value(row, "Admission Deadline"), "scholarship": value(row, "Scholarship"), "admission_mode": value(row, "Admission Mode"), "brochure_url": value(row, "Brochure URL"), "seo_title": value(row, "SEO Title"), "seo_description": value(row, "SEO Description"), "seo_keywords": value(row, "SEO Keywords"), "seo_slug": value(row, "SEO Slug"),
            "external_image_url": value(row, "External Image URL"), "image_source_url": value(row, "Image Source URL"),
            "featured": as_bool(value(row, "Featured"), False), "active": as_bool(value(row, "Active"), True)})
        requested = split_courses(value(row, "Courses"))
        found, missing = [], []
        for course_name in requested:
            course = Course.objects.filter(name__iexact=course_name).first()
            (found if course else missing).append(course or course_name)
        if missing: raise ValidationError("Courses not found: " + ", ".join(missing))
        if requested: obj.courses.set(found)
        validate_image_references([value(row, "Image Filename")], images)
        image_count = attach_image(obj, "image", value(row, "Image Filename"), images)
        gallery_names = split_courses(value(row, "Gallery Image Filenames"))
        validate_image_references(gallery_names, images)
        if gallery_names:
            obj.gallery_images.all().delete()
            for gallery_name in gallery_names:
                safe_name = PurePosixPath(gallery_name).name
                original_name, data = images[safe_name.casefold()]
                gallery = CollegeImage(college=obj)
                gallery.image.save(original_name, ContentFile(data), save=True)
                image_count += 1
        return ("updated" if existing else "created"), key, image_count

    title = value(row, "Title"); key = title
    if not title: raise ValidationError("Title is required")
    existing = OnlineCourse.objects.filter(title__iexact=title).first()
    if existing and mode == "create": return "skipped", key, 0
    obj = existing or OnlineCourse(title=title)
    save_object(obj, {"title": title, "category": valid_choice(value(row, "Category"), OnlineCourse.CATEGORIES, "category", "Skill Development"),
        "provider": value(row, "Provider"), "specialization": value(row, "Specialization"), "short_description": value(row, "Short Description"), "description": value(row, "Career Path") or value(row, "Description"), "motivation": value(row, "Motivation"), "duration": value(row, "Duration"), "fee": value(row, "Fee"),
        "eligibility": value(row, "Eligibility"), "accreditation": value(row, "Accreditation"), "exam_mode": value(row, "Exam Mode"), "lms_details": value(row, "LMS Details"),
        "external_image_url": value(row, "External Image URL"), "image_source_url": value(row, "Image Source URL"), "external_url": value(row, "Course URL"), "application_url": value(row, "Application URL"), "brochure_url": value(row, "Brochure URL"), "seo_title": value(row, "SEO Title"), "seo_description": value(row, "SEO Description"), "seo_keywords": value(row, "SEO Keywords"), "seo_slug": value(row, "SEO Slug"),
        "featured": as_bool(value(row, "Featured"), False), "active": as_bool(value(row, "Active"), True)})
    validate_image_references([value(row, "Image Filename")], images)
    image_count = attach_image(obj, "image", value(row, "Image Filename"), images)
    return ("updated" if existing else "created"), key, image_count


def dataset_records(dataset):
    if dataset == "leads": return Lead.objects.select_related("course", "preferred_college", "assigned_to").order_by("-created_at")
    if dataset == "courses": return Course.objects.order_by("name")
    if dataset == "colleges": return College.objects.exclude(college_type="Medical").prefetch_related("courses").order_by("name")
    if dataset == "medical_colleges": return College.objects.filter(college_type="Medical").prefetch_related("courses").order_by("name")
    if dataset == "online_courses": return OnlineCourse.objects.order_by("title")
    raise ValueError("Unknown dataset")


def image_name(field):
    return PurePosixPath(field.name).name if field and field.name else ""


def export_values(dataset, obj):
    if dataset == "leads": return [obj.name, obj.father_name, obj.phone, obj.email, obj.city, str(obj.course or ""), str(obj.preferred_college or ""), obj.class_10_percentage or "", obj.class_12_percentage or "", obj.score, obj.source, obj.status, obj.call_outcome, obj.assigned_to.username if obj.assigned_to else "", "Yes" if obj.consent else "No"]
    if dataset == "courses": return [obj.name, obj.category, obj.level, obj.duration, obj.specialization, obj.eligibility, obj.entrance_exam, obj.annual_fee, obj.total_fee, obj.seats or "", obj.short_description, obj.career_description, obj.motivation, obj.brochure_url, obj.seo_title, obj.seo_description, obj.seo_keywords, obj.seo_slug, image_name(obj.image), obj.external_image_url, obj.image_source_url]
    if dataset in {"colleges", "medical_colleges"}:
        base = [obj.name, obj.university, obj.university_group]
        if dataset == "colleges": base.append(obj.college_type)
        return base + [obj.city, obj.state, obj.address, obj.website, obj.phone, obj.email, ", ".join(obj.courses.values_list("name", flat=True)), obj.short_description, obj.description, obj.motivation, obj.approvals, obj.ranking, obj.accreditation, obj.average_package, obj.highest_package, obj.hostel, obj.admission_deadline, obj.scholarship, obj.admission_mode, obj.brochure_url, obj.seo_title, obj.seo_description, obj.seo_keywords, obj.seo_slug, image_name(obj.image), ", ".join(image_name(x.image) for x in obj.gallery_images.all()), obj.external_image_url, obj.image_source_url, "Yes" if obj.featured else "No", "Yes" if obj.active else "No"]
    return [obj.title, obj.category, obj.provider, obj.specialization, obj.short_description, obj.description, obj.motivation, obj.duration, obj.fee, obj.eligibility, obj.accreditation, obj.exam_mode, obj.lms_details, obj.external_url, obj.application_url, obj.brochure_url, obj.seo_title, obj.seo_description, obj.seo_keywords, obj.seo_slug, image_name(obj.image), obj.external_image_url, obj.image_source_url, "Yes" if obj.featured else "No", "Yes" if obj.active else "No"]


def make_tabular_response(dataset, file_format, records=None, template=False):
    from django.http import HttpResponse
    spec = DATASETS[dataset]; rows = [spec["sample"]] if template else [export_values(dataset, obj) for obj in (records or dataset_records(dataset))]
    suffix = "template" if template else "export"; filename = f"{dataset}-{suffix}.{file_format}"
    if file_format == "csv":
        response = HttpResponse(content_type="text/csv; charset=utf-8"); response.write("\ufeff")
        writer = csv.writer(response); writer.writerow(spec["headers"]); writer.writerows(rows)
    elif file_format == "xlsx":
        book = Workbook(); sheet = book.active; sheet.title = spec["title"][:31]; sheet.append(spec["headers"])
        for row in rows: sheet.append(row)
        sheet.freeze_panes = "A2"; sheet.auto_filter.ref = sheet.dimensions
        for cell in sheet[1]: cell.font = cell.font.copy(bold=True)
        for column in sheet.columns: sheet.column_dimensions[column[0].column_letter].width = min(max(len(str(cell.value or "")) for cell in column) + 2, 35)
        stream = io.BytesIO(); book.save(stream)
        response = HttpResponse(stream.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else: raise ValueError("Only CSV and XLSX are supported")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
