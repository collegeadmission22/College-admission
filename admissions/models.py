from django.contrib.auth.models import User
from django.db import models
import re


# ============================================================
# COURSE
# Media:
# media/courses/
# ============================================================

class Course(models.Model):

    CATEGORIES = [
        (x, x)
        for x in [
            "Engineering",
            "Management",
            "Computer Applications",
            "Law",
            "Media",
            "Pharmacy",
            "Medical",
            "Commerce",
            "Education",
            "Other",
        ]
    ]

    LEVELS = [
        ("UG", "Undergraduate"),
        ("PG", "Postgraduate"),
        ("DIP", "Diploma"),
    ]

    name = models.CharField(max_length=100)

    category = models.CharField(
        max_length=40,
        choices=CATEGORIES,
        default="Other",
    )

    college_categories = models.ManyToManyField(
        "CollegeCategory",
        blank=True,
        related_name="courses_by_category",
        verbose_name="College Categories",
        help_text="Select one or more college categories for this course.",
    )

    course_categories = models.ManyToManyField(
        "CourseCategoryMaster",
        blank=True,
        related_name="courses",
        verbose_name="Course Categories",
        help_text="Select one or more course categories.",
    )

    level = models.CharField(
        max_length=30,
        choices=LEVELS,
        default="UG",
    )

    duration = models.CharField(
        max_length=30,
        blank=True,
    )

    image = models.ImageField(
        upload_to="courses/",
        blank=True,
        null=True,
    )

    external_image_url = models.URLField(
        blank=True,
        help_text="AI-generated or licensed course image URL",
    )

    image_source_url = models.URLField(
        blank=True,
        help_text="Credit/source page for external image",
    )

    short_description = models.CharField(
        max_length=220,
        blank=True,
    )

    career_description = models.TextField(
        "Career path",
        blank=True,
    )

    motivation = models.CharField(
        max_length=180,
        blank=True,
    )

    specialization = models.CharField(
        max_length=160,
        blank=True,
    )

    eligibility = models.TextField(
        blank=True,
    )

    entrance_exam = models.CharField(
        max_length=160,
        blank=True,
    )

    annual_fee = models.CharField(
        max_length=80,
        blank=True,
    )

    total_fee = models.CharField(
        max_length=80,
        blank=True,
    )

    seats = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    brochure_url = models.URLField(
        blank=True,
    )

    seo_title = models.CharField(
        max_length=180,
        blank=True,
    )

    seo_description = models.CharField(
        max_length=320,
        blank=True,
    )

    seo_keywords = models.TextField(
        blank=True,
        help_text="Comma-separated SEO keywords.",
    )

    seo_slug = models.SlugField(
        max_length=220,
        blank=True,
        db_index=True,
        help_text="SEO-friendly URL slug.",
    )

    def __str__(self):
        return self.name


# ============================================================
# COLLEGE
#
# Main image:
# media/colleges/
#
# Logo:
# media/college_logos/
# ============================================================

class CollegeCategory(models.Model):
    """Categories a college can belong to. A college may select more than one."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)

    class Meta:
        verbose_name_plural = "College categories"
        ordering = ("name",)

    def __str__(self):
        return self.name


class College(models.Model):

    GROUPS = [
        ("IPU", "IPU Colleges"),
        ("MDU", "MDU Colleges"),
        ("AKTU", "AKTU Colleges"),
        ("KUK", "KUK Colleges"),
        ("OTHER", "Other Colleges"),
    ]

    TYPES = [
        ("Medical", "Medical Colleges"),
        ("Management", "Management Colleges"),
        ("Law", "Law Colleges"),
        ("Engineering", "Engineering Colleges"),
        ("Media", "Media Colleges"),
        ("International", "International Colleges"),
    ]

    name = models.CharField(
        max_length=180,
    )

    university = models.ForeignKey(
        "UniversityMaster",
        verbose_name="University Name",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="colleges",
    )

    university_group = models.CharField(
        max_length=10,
        choices=GROUPS,
        default="OTHER",
    )

    college_type = models.CharField(
        "College Category",
        max_length=30,
        choices=TYPES,
        default="Engineering",
    )

    categories = models.ManyToManyField(
        CollegeCategory,
        blank=True,
        related_name="colleges",
        help_text="Select one or more: Engineering, Management, Law, Pharmacy, Medical, etc.",
    )

    city = models.CharField(
        max_length=80,
        default="New Delhi",
    )

    state = models.ForeignKey(
        "StateMaster",
        verbose_name="State",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="colleges",
    )

    country = models.ForeignKey(
        "CountryMaster",
        verbose_name="Country",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="colleges",
        help_text="Optional. State and Country can be selected independently.",
    )

    courses = models.ManyToManyField(
        Course,
        blank=True,
    )

    short_description = models.CharField(
        max_length=220,
        blank=True,
        help_text="Short card summary for the college.",
    )

    description = models.TextField(
        "Career path",
        blank=True,
        help_text="Career opportunities and professional pathways for students.",
    )

    motivation = models.CharField(
        max_length=220,
        blank=True,
        help_text="Motivational line shown on the college card/page.",
    )

    image = models.ImageField(
        upload_to="colleges/",
        blank=True,
        null=True,
    )

    external_image_url = models.URLField(
        blank=True,
        help_text="Licensed campus image URL, e.g. Wikimedia Commons",
    )

    image_source_url = models.URLField(
        blank=True,
        help_text="Original image/source page for attribution",
    )

    featured = models.BooleanField(
        default=False,
    )

    active = models.BooleanField(
        default=True,
    )

    address = models.TextField(
        blank=True,
    )

    website = models.URLField(
        blank=True,
    )

    phone = models.CharField(
        max_length=40,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    approvals = models.CharField(
        max_length=240,
        blank=True,
    )

    ranking = models.CharField(
        max_length=240,
        blank=True,
    )

    accreditation = models.CharField(
        max_length=160,
        blank=True,
    )

    average_package = models.CharField(
        max_length=80,
        blank=True,
    )

    highest_package = models.CharField(
        max_length=80,
        blank=True,
    )

    hostel = models.CharField(
        max_length=160,
        blank=True,
    )

    admission_deadline = models.CharField(
        max_length=120,
        blank=True,
    )

    scholarship = models.TextField(
        blank=True,
    )

    admission_mode = models.CharField(
        max_length=160,
        blank=True,
    )

    brochure_url = models.URLField(
        blank=True,
    )

    seo_title = models.CharField(
        max_length=180,
        blank=True,
    )

    seo_description = models.CharField(
        max_length=320,
        blank=True,
    )

    seo_keywords = models.TextField(
        blank=True,
        help_text="Comma-separated SEO keywords.",
    )

    seo_slug = models.SlugField(
        max_length=220,
        blank=True,
        db_index=True,
        help_text="SEO-friendly URL slug.",
    )

    def __str__(self):
        return self.name


# ============================================================
# COLLEGE GALLERY
# Media:
# media/college_gallery/
# ============================================================

class CollegeImage(models.Model):

    college = models.ForeignKey(
        College,
        related_name="gallery_images",
        on_delete=models.CASCADE,
    )

    image = models.ImageField(
        upload_to="college_gallery/",
    )

    caption = models.CharField(
        max_length=180,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.college.name} gallery image"


# ============================================================
# LEAD
#
# Documents:
# media/leads/YYYY/MM/
# ============================================================

class Lead(models.Model):

    STATUS = [
        (x, x)
        for x in [
            "New Enquiry",
            "New",
            "First Call",
            "Contacted",
            "Interested",
            "Hot",
            "Warm",
            "Cold",
            "Visit Planned",
            "Counselling Booked",
            "Counselling Done",
            "Documents Pending",
            "Application Started",
            "Application Submitted",
            "Offer Issued",
            "Fee Pending",
            "Fee Paid",
            "Registered",
            "Admission Confirmed",
            "Closed",
            "Lost",
        ]
    ]

    CALL_OUTCOMES = [
        (x, x)
        for x in [
            "Untouched",
            "Connected",
            "Not Reachable",
            "Busy",
            "Call Again",
            "Parent Discussion",
            "Interested",
            "Not Interested",
            "Visit Planned",
            "Registered",
        ]
    ]

    SOURCE = [
        (x, x)
        for x in [
            "Website",
            "Google Ads",
            "Facebook",
            "Facebook Messenger",
            "Instagram",
            "Instagram Messenger",
            "WhatsApp",
            "WhatsApp Chatbot",
            "AI Chatbot",
            "Contact Form",
            "Phone Call",
            "Walk-in",
            "Referral",
            "YouTube",
            "LinkedIn",
            "Other",
        ]
    ]

    name = models.CharField(
        max_length=120,
    )

    father_name = models.CharField(
        max_length=120,
        blank=True,
    )

    phone = models.CharField(
        max_length=20,
        unique=True,
        help_text="Unique mobile number used to prevent duplicate leads",
    )

    email = models.EmailField(
        blank=True,
    )

    city = models.CharField(
        max_length=80,
        blank=True,
    )

    course = models.ForeignKey(
        Course,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    preferred_college = models.ForeignKey(
        College,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    preferred_distance_online = models.ForeignKey(
        "DistanceOnlineEducation",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="leads",
        verbose_name="Distance / Online Education",
    )

    score = models.CharField(
        "Entrance score/rank",
        max_length=80,
        blank=True,
    )

    class_10_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    class_12_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    LEAD_CATEGORIES = [(x, x) for x in ["Hot", "Warm", "Cold", "Fresh", "Follow-up", "Admission Ready", "Converted", "Lost"]]

    lead_category = models.CharField(
        max_length=30, choices=LEAD_CATEGORIES, default="Fresh", db_index=True,
        help_text="Lead priority/category used by counsellors for nurturing and conversion."
    )

    source = models.CharField(
        max_length=30,
        choices=SOURCE,
        default="Website",
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS,
        default="New Enquiry",
    )

    call_outcome = models.CharField(
        max_length=30,
        choices=CALL_OUTCOMES,
        default="Untouched",
    )

    next_action = models.CharField(
        max_length=220,
        blank=True,
    )

    last_contacted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    assigned_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    uploaded_by = models.ForeignKey(
        User,
        related_name="uploaded_leads",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # Lead document/file upload
    document = models.FileField(
        upload_to="leads/%Y/%m/",
        blank=True,
        null=True,
    )

    consent = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["status", "created_at"]
            ),
            models.Index(
                fields=["assigned_to", "status"]
            ),
            models.Index(
                fields=["source", "created_at"]
            ),
        ]

    def __str__(self):
        return f"{self.name} - {self.phone}"

    def save(self, *args, **kwargs):

        digits = re.sub(
            r"\D",
            "",
            self.phone or "",
        )

        self.phone = (
            digits[-10:]
            if len(digits) >= 10
            else digits
        )

        super().save(*args, **kwargs)


# ============================================================
# LEAD ACTIVITY
# ============================================================

class LeadActivity(models.Model):

    lead = models.ForeignKey(
        Lead,
        related_name="activities",
        on_delete=models.CASCADE,
    )

    activity_type = models.CharField(
        max_length=40,
        choices=[
            (x, x)
            for x in [
                "Created",
                "Stage Changed",
                "Call",
                "Follow-up",
                "Note",
                "Assignment",
                "Communication",
                "Admission",
            ]
        ],
    )

    description = models.TextField()

    old_stage = models.CharField(
        max_length=30,
        blank=True,
    )

    new_stage = models.CharField(
        max_length=30,
        blank=True,
    )

    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.lead.name} · {self.activity_type}"


# ============================================================
# LEAD REMARK
# ============================================================

class LeadRemark(models.Model):

    lead = models.ForeignKey(
        Lead,
        related_name="remarks",
        on_delete=models.CASCADE,
    )

    remark = models.TextField()

    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.lead.name} · {self.created_at:%d %b %Y}"


# ============================================================
# NURTURE LOG
# ============================================================

class NurtureLog(models.Model):

    lead = models.ForeignKey(
        Lead,
        related_name="nurture_logs",
        on_delete=models.CASCADE,
    )

    day = models.PositiveSmallIntegerField()

    status = models.CharField(
        max_length=20,
        choices=[
            (x, x)
            for x in [
                "Queued",
                "Sent",
                "Partial",
                "Failed",
                "Skipped",
            ]
        ],
    )

    details = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["lead", "day"],
                name="unique_lead_nurture_day",
            )
        ]


# ============================================================
# USER PROFILE
# ============================================================

class UserProfile(models.Model):

    ROLES = [
        (x, x)
        for x in [
            "Admin",
            "Super Admin",
            "Admission Manager",
            "Counsellor",
            "Data Entry Operator",
            "Staff",
            "Employee",
            "Agent",
            "Consultant",
            "College",
        ]
    ]

    user = models.OneToOneField(
        User,
        related_name="crm_profile",
        on_delete=models.CASCADE,
    )

    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default="Employee",
    )

    college = models.ForeignKey(
        "College",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    organisation = models.CharField(
        max_length=140,
        blank=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    active = models.BooleanField(
        default=True,
    )

    can_import_leads = models.BooleanField(
        default=False,
    )

    can_export_leads = models.BooleanField(
        default=False,
    )

    can_add_own_leads = models.BooleanField(
        default=True,
        help_text="Allow this user to add leads to their own CRM panel."
    )

    def __str__(self):
        return f"{self.user.username} · {self.role}"


# ============================================================
# CRM API KEY
# ============================================================

class CRMApiKey(models.Model):

    owner = models.ForeignKey(
        User,
        related_name="crm_api_keys",
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=100,
    )

    prefix = models.CharField(
        max_length=16,
        db_index=True,
    )

    key_hash = models.CharField(
        max_length=64,
        unique=True,
    )

    active = models.BooleanField(
        default=True,
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_by = models.ForeignKey(
        User,
        related_name="created_crm_api_keys",
        null=True,
        on_delete=models.SET_NULL,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    last_used_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name} · {self.prefix}…"


# ============================================================
# LEAD IMPORT BATCH
# ============================================================

class LeadImportBatch(models.Model):

    uploaded_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
    )

    file_name = models.CharField(
        max_length=255,
    )

    assigned_to = models.ForeignKey(
        User,
        related_name="import_batches_assigned",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    total_rows = models.PositiveIntegerField(
        default=0,
    )

    created_count = models.PositiveIntegerField(
        default=0,
    )

    updated_count = models.PositiveIntegerField(
        default=0,
    )

    rejected_count = models.PositiveIntegerField(
        default=0,
    )

    error_report = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.file_name} · {self.created_at:%d %b %Y}"


# ============================================================
# BULK DATA BATCH
# ============================================================

class BulkDataBatch(models.Model):

    DATASETS = [
        (x, x.replace("_", " ").title())
        for x in [
            "leads",
            "courses",
            "colleges",
            "medical_colleges",
            "online_courses",
        ]
    ]

    MODES = [
        ("create", "Create new only"),
        ("upsert", "Create and update"),
    ]

    dataset = models.CharField(
        max_length=30,
        choices=DATASETS,
    )

    mode = models.CharField(
        max_length=10,
        choices=MODES,
        default="upsert",
    )

    file_name = models.CharField(
        max_length=255,
    )

    uploaded_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
    )

    total_rows = models.PositiveIntegerField(default=0)
    created_count = models.PositiveIntegerField(default=0)
    updated_count = models.PositiveIntegerField(default=0)
    skipped_count = models.PositiveIntegerField(default=0)
    rejected_count = models.PositiveIntegerField(default=0)

    imported_image_count = models.PositiveIntegerField(
        default=0,
    )

    error_report = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.get_dataset_display()} · {self.file_name}"


# ============================================================
# COMMUNICATION
# ============================================================

class Communication(models.Model):

    CHANNELS = [
        (x, x)
        for x in [
            "Email",
            "WhatsApp",
            "SMS",
            "RCS",
        ]
    ]

    STATUSES = [
        (x, x)
        for x in [
            "Draft",
            "Queued",
            "Sent",
            "Delivered",
            "Read",
            "Failed",
        ]
    ]

    lead = models.ForeignKey(
        Lead,
        related_name="communications",
        on_delete=models.CASCADE,
    )

    channel = models.CharField(
        max_length=20,
        choices=CHANNELS,
    )

    subject = models.CharField(
        max_length=180,
        blank=True,
    )

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUSES,
        default="Draft",
    )

    provider_message_id = models.CharField(
        max_length=180,
        blank=True,
    )

    provider_response = models.TextField(
        blank=True,
    )

    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return (
            f"{self.channel} · "
            f"{self.lead.name} · "
            f"{self.status}"
        )


# ============================================================
# COMMUNICATION TEMPLATE
# ============================================================

class CommunicationTemplate(models.Model):

    CHANNELS = Communication.CHANNELS

    name = models.CharField(
        max_length=120,
    )

    channel = models.CharField(
        max_length=20,
        choices=CHANNELS,
    )

    subject = models.CharField(
        max_length=180,
        blank=True,
    )

    message = models.TextField(
        help_text=(
            "Merge fields: "
            "{name}, {course}, {college}, {counsellor}"
        )
    )

    active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return f"{self.name} · {self.channel}"


# ============================================================
# STUDENT APPLICATION
# ============================================================

class StudentApplication(models.Model):

    STATUS = [
        (x, x)
        for x in [
            "Draft",
            "Submitted",
            "Under Review",
            "Documents Required",
            "Approved",
            "Rejected",
        ]
    ]

    user = models.OneToOneField(
        User,
        related_name="student_application",
        on_delete=models.CASCADE,
    )

    full_name = models.CharField(
        max_length=120,
    )

    father_name = models.CharField(
        max_length=120,
        blank=True,
    )

    phone = models.CharField(
        max_length=20,
    )

    email = models.EmailField()

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    gender = models.CharField(
        max_length=20,
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    city = models.CharField(
        max_length=80,
        blank=True,
    )

    state = models.CharField(
        max_length=80,
        blank=True,
    )

    pincode = models.CharField(
        max_length=10,
        blank=True,
    )

    course = models.ForeignKey(
        Course,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    college = models.ForeignKey(
        College,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class_10_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    class_12_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    entrance_exam = models.CharField(
        max_length=50,
        blank=True,
    )

    entrance_rank = models.CharField(
        max_length=50,
        blank=True,
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS,
        default="Draft",
    )

    declaration = models.BooleanField(
        default=False,
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"Application - {self.full_name}"


# ============================================================
# STUDENT DOCUMENT
#
# Media:
# media/student_documents/YYYY/MM/
# ============================================================

class StudentDocument(models.Model):

    TYPES = [
        (x, x)
        for x in [
            "Photograph",
            "Signature",
            "Aadhaar Card",
            "Class 10 Marksheet",
            "Class 12 Marksheet",
            "Entrance Scorecard",
            "Character Certificate",
            "Migration Certificate",
            "Certificate",
            "Resume",
            "Other",
        ]
    ]

    application = models.ForeignKey(
        StudentApplication,
        related_name="documents",
        on_delete=models.CASCADE,
    )

    document_type = models.CharField(
        max_length=40,
        choices=TYPES,
    )

    file = models.FileField(
        upload_to="student_documents/%Y/%m/",
    )

    verified = models.BooleanField(
        default=False,
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"{self.application.full_name} - "
            f"{self.document_type}"
        )


# ============================================================
# STUDENT PAYMENT
# ============================================================

class StudentPayment(models.Model):

    application = models.ForeignKey(
        StudentApplication,
        related_name="payments",
        on_delete=models.CASCADE,
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=20,
        choices=[
            (x, x)
            for x in [
                "Pending",
                "Part Paid",
                "Paid",
                "Refunded",
            ]
        ],
        default="Pending",
    )

    reference = models.CharField(
        max_length=100,
        blank=True,
    )

    due_date = models.DateField(
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )


# ============================================================
# STUDENT NOTIFICATION
# ============================================================

class StudentNotification(models.Model):

    user = models.ForeignKey(
        User,
        related_name="student_notifications",
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        max_length=150,
    )

    message = models.TextField()

    read = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )


# ============================================================
# CONTACT MESSAGE
# ============================================================

class ContactMessage(models.Model):

    name = models.CharField(
        max_length=120,
    )

    phone = models.CharField(
        max_length=20,
    )

    email = models.EmailField(
        blank=True,
    )

    subject = models.CharField(
        max_length=150,
        blank=True,
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.name


# ============================================================
# SOCIAL LINKS
# ============================================================

class SocialLink(models.Model):

    PLATFORMS = [
        (x, x)
        for x in [
            "Facebook",
            "Instagram",
            "YouTube",
            "LinkedIn",
        ]
    ]

    platform = models.CharField(
        max_length=20,
        choices=PLATFORMS,
        unique=True,
    )

    page_name = models.CharField(
        max_length=100,
        blank=True,
    )

    url = models.URLField(
        blank=True,
    )

    active = models.BooleanField(
        default=True,
    )

    display_order = models.PositiveSmallIntegerField(
        default=0,
    )

    def __str__(self):
        return self.platform


# ============================================================
# ONLINE COURSE
#
# Media:
# media/online_courses/
# ============================================================

class OnlineCourse(models.Model):

    CATEGORIES = [
        (x, x)
        for x in [
            "Engineering",
            "Management",
            "Computer Applications",
            "Law",
            "Media",
            "Pharmacy",
            "Medical",
            "Commerce",
            "Skill Development",
        ]
    ]

    title = models.CharField(
        max_length=150,
    )

    category = models.CharField(
        max_length=40,
        choices=CATEGORIES,
    )

    provider = models.CharField(
        max_length=120,
        blank=True,
    )

    short_description = models.CharField(
        max_length=220,
        blank=True,
        help_text="Short card summary for the online course.",
    )

    description = models.TextField(
        "Career path",
        blank=True,
        help_text="Career opportunities and professional pathways after this online course.",
    )

    motivation = models.CharField(
        max_length=220,
        blank=True,
        help_text="Motivational line shown on the online course card/page.",
    )

    duration = models.CharField(
        max_length=50,
        blank=True,
    )

    fee = models.CharField(
        max_length=50,
        blank=True,
    )

    image = models.ImageField(
        upload_to="online_courses/",
        blank=True,
        null=True,
    )

    external_image_url = models.URLField(
        blank=True,
    )

    image_source_url = models.URLField(
        blank=True,
    )

    external_url = models.URLField(
        blank=True,
    )

    featured = models.BooleanField(
        default=False,
    )

    active = models.BooleanField(
        default=True,
    )

    eligibility = models.TextField(
        blank=True,
    )

    accreditation = models.CharField(
        max_length=180,
        blank=True,
    )

    exam_mode = models.CharField(
        max_length=120,
        blank=True,
    )

    lms_details = models.TextField(
        blank=True,
    )

    specialization = models.CharField(
        max_length=180,
        blank=True,
    )

    application_url = models.URLField(
        blank=True,
    )

    brochure_url = models.URLField(
        blank=True,
    )

    seo_title = models.CharField(
        max_length=180,
        blank=True,
    )

    seo_description = models.CharField(
        max_length=320,
        blank=True,
    )

    seo_keywords = models.TextField(
        blank=True,
        help_text="Comma-separated SEO keywords.",
    )

    seo_slug = models.SlugField(
        max_length=220,
        blank=True,
        db_index=True,
        help_text="SEO-friendly URL slug.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.title


# ============================================================
# SOCIAL CLICK
# ============================================================

class SocialClick(models.Model):

    platform = models.CharField(
        max_length=20,
    )

    source_page = models.CharField(
        max_length=200,
        blank=True,
    )

    clicked_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"{self.platform} - "
            f"{self.clicked_at:%d %b %Y}"
        )


# ============================================================
# CHAT MESSAGE
# ============================================================

class ChatMessage(models.Model):

    session_key = models.CharField(
        max_length=80,
        db_index=True,
    )

    user_message = models.TextField()

    bot_response = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.user_message[:50]


# ============================================================
# SITE SETTINGS
#
# Media:
# media/branding/
# ============================================================

class DistanceOnlineEducation(models.Model):
    """Distance / Online Education catalogue managed from CRM/Admin."""
    name = models.CharField(max_length=180)
    university = models.ForeignKey("UniversityMaster", on_delete=models.SET_NULL, null=True, blank=True, related_name="distance_online_programmes")
    state = models.ForeignKey("StateMaster", on_delete=models.SET_NULL, null=True, blank=True, related_name="distance_online_programmes")
    country = models.ForeignKey("CountryMaster", on_delete=models.SET_NULL, null=True, blank=True, related_name="distance_online_programmes")
    categories = models.ManyToManyField("CollegeCategory", blank=True, related_name="distance_online_programmes")
    short_description = models.CharField(max_length=220, blank=True)
    description = models.TextField("Career path", blank=True)
    motivation = models.CharField(max_length=180, blank=True)
    image = models.ImageField(upload_to="distance_online/", blank=True, null=True)
    seo_title = models.CharField(max_length=180, blank=True)
    seo_description = models.CharField(max_length=320, blank=True)
    seo_keywords = models.TextField(blank=True)
    seo_slug = models.SlugField(max_length=220, blank=True, db_index=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Distance / Online Education"
        verbose_name_plural = "Distance / Online Education"
        ordering = ("name",)

    def __str__(self):
        return self.name


class SiteSettings(models.Model):

    header_logo = models.ImageField(
        upload_to="branding/",
        blank=True,
        null=True,
    )

    home_logo = models.ImageField(
        upload_to="branding/",
        blank=True,
        null=True,
        help_text="Optional College Admission logo displayed on the home page.",
    )

    logo_alt_text = models.CharField(
        max_length=100,
        default="College Admission",
    )

    apply_popup_enabled = models.BooleanField(
        default=True,
    )

    auto_open_popup = models.BooleanField(
        default=True,
    )

    popup_title = models.CharField(
        max_length=120,
        default="Apply for Admission",
    )

    popup_message = models.CharField(
        max_length=240,
        default=(
            "Complete the short form for free counselling "
            "and application assistance."
        ),
    )

    popup_delay_seconds = models.PositiveSmallIntegerField(
        default=5,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name_plural = "Site settings"

    def __str__(self):
        return "Portal settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


# ============================================================
# FOLLOW UP
# ============================================================

class FollowUp(models.Model):

    lead = models.ForeignKey(
        Lead,
        related_name="followups",
        on_delete=models.CASCADE,
    )

    due_at = models.DateTimeField()

    note = models.TextField()

    completed = models.BooleanField(
        default=False,
    )

    outcome = models.CharField(
        max_length=220,
        blank=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    reminder_minutes_before = models.PositiveIntegerField(
        default=30,
    )

    notify_assignee_email = models.BooleanField(
        default=True,
    )

    notify_lead_whatsapp = models.BooleanField(
        default=False,
    )

    notify_lead_sms = models.BooleanField(
        default=False,
    )

    reminder_sent_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    reminder_result = models.TextField(
        blank=True,
    )

    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["completed", "due_at"]
            ),
            models.Index(
                fields=["reminder_sent_at", "due_at"]
            ),
        ]

    def __str__(self):
        return f"{self.lead.name} - {self.due_at:%d %b %Y}"


# ============================================================
# MODULE ACCESS
# ============================================================

class ModuleAccess(models.Model):

    MODULES = [
        (x, x.replace("_", " ").title())
        for x in [
            "college",
            "course",
            "online_course",
            "student",
            "medical_college",
            "social_seo",
            "entrance_exam",
            "classroom",
            "employee_hr",
            "counsellor_calling",
            "leads",
            "communications",
            "finance",
            "tasks",
            "reports",
            "partners",
            "roles",
        ]
    ]

    user = models.ForeignKey(
        User,
        related_name="module_permissions",
        on_delete=models.CASCADE,
    )

    module = models.CharField(
        max_length=40,
        choices=MODULES,
    )

    can_view = models.BooleanField(default=True)
    can_add = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    can_import = models.BooleanField(default=False)
    can_export = models.BooleanField(default=False)
    can_assign = models.BooleanField(default=False)
    can_approve = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "module"],
                name="unique_user_module_access",
            )
        ]

    def __str__(self):
        return (
            f"{self.user.username} · "
            f"{self.get_module_display()}"
        )


# ============================================================
# ENTRANCE EXAM
# ============================================================

class EntranceExam(models.Model):

    name = models.CharField(
        max_length=120,
    )

    short_name = models.CharField(
        max_length=40,
        blank=True,
    )

    level = models.CharField(
        max_length=60,
        blank=True,
    )

    conducting_body = models.CharField(
        max_length=160,
        blank=True,
    )

    application_start = models.DateField(
        null=True,
        blank=True,
    )

    application_end = models.DateField(
        null=True,
        blank=True,
    )

    exam_date = models.DateField(
        null=True,
        blank=True,
    )

    website = models.URLField(
        blank=True,
    )

    eligibility = models.TextField(
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return self.short_name or self.name


# ============================================================
# CLASSROOM
# ============================================================

class Classroom(models.Model):

    title = models.CharField(
        max_length=160,
    )

    course = models.ForeignKey(
        Course,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    trainer = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    start_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    meeting_url = models.URLField(
        blank=True,
    )

    room = models.CharField(
        max_length=100,
        blank=True,
    )

    capacity = models.PositiveIntegerField(
        default=0,
    )

    active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return self.title


# ============================================================
# SOCIAL SEO ITEM
# ============================================================

class SocialSEOItem(models.Model):

    PLATFORMS = [
        (x, x)
        for x in [
            "Website",
            "Google",
            "YouTube",
            "Facebook",
            "Instagram",
            "LinkedIn",
            "Other",
        ]
    ]

    platform = models.CharField(
        max_length=30,
        choices=PLATFORMS,
    )

    title = models.CharField(
        max_length=180,
    )

    target_url = models.URLField(
        blank=True,
    )

    keyword = models.CharField(
        max_length=220,
        blank=True,
    )

    status = models.CharField(
        max_length=30,
        default="Draft",
    )

    scheduled_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    impressions = models.PositiveIntegerField(
        default=0,
    )

    clicks = models.PositiveIntegerField(
        default=0,
    )

    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.platform} · {self.title}"


# ============================================================
# EMPLOYEE RECORD
# ============================================================

class EmployeeRecord(models.Model):

    user = models.OneToOneField(
        User,
        related_name="employee_record",
        on_delete=models.CASCADE,
    )

    designation = models.CharField(
        max_length=100,
        blank=True,
    )

    department = models.CharField(
        max_length=100,
        blank=True,
    )

    manager = models.ForeignKey(
        User,
        related_name="team_members",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    joining_date = models.DateField(
        null=True,
        blank=True,
    )

    active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return (
            self.user.get_full_name()
            or self.user.username
        )


# ============================================================
# CRM TASK
# ============================================================

class CRMTask(models.Model):

    title = models.CharField(
        max_length=180,
    )

    description = models.TextField(
        blank=True,
    )

    assigned_to = models.ForeignKey(
        User,
        related_name="crm_tasks",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    lead = models.ForeignKey(
        Lead,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    due_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    priority = models.CharField(
        max_length=20,
        default="Normal",
    )

    status = models.CharField(
        max_length=30,
        default="Open",
    )

    created_by = models.ForeignKey(
        User,
        related_name="created_crm_tasks",
        null=True,
        on_delete=models.SET_NULL,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.title
# ============================================================
# ADMISSION MASTER DATA
# Editable lookup lists for Admissions Administration.
# ============================================================
class CountryMaster(models.Model):
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)
    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ("name",)
    def __str__(self): return self.name

class StateMaster(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(CountryMaster, null=True, blank=True, on_delete=models.SET_NULL, related_name="states")
    active = models.BooleanField(default=True)
    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"
        ordering = ("country__name", "name")
        constraints = [models.UniqueConstraint(fields=("country", "name"), name="unique_state_per_country")]
    def __str__(self): return f"{self.name}, {self.country.name}" if self.country else self.name

class UniversityMaster(models.Model):
    name = models.CharField(max_length=180, unique=True)
    state = models.ForeignKey(StateMaster, null=True, blank=True, on_delete=models.SET_NULL, related_name="universities")
    active = models.BooleanField(default=True)
    class Meta:
        verbose_name = "University Name"
        verbose_name_plural = "University Names"
        ordering = ("name",)
    def __str__(self): return self.name

class CourseCategoryMaster(models.Model):
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)
    class Meta:
        verbose_name = "Course Category"
        verbose_name_plural = "Course Categories"
        ordering = ("name",)
    def __str__(self): return self.name

# ============================================================
# ADDITIONAL INFORMATION PAGES
# Keeps the main College/Course CRM simple while allowing rich detail pages.
# ============================================================
class CollegeAdditionalInformation(models.Model):
    college = models.OneToOneField(College, on_delete=models.CASCADE, related_name="additional_information")
    overview = models.TextField(blank=True, help_text="Additional text shown on the college detail page.")
    campus_tour_url = models.URLField("Campus Tours", blank=True, help_text="Campus tour video or virtual campus tour URL.")
    placement = models.TextField(blank=True, help_text="Placement details, recruiters and package information.")
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "College Additional Information"
        verbose_name_plural = "College Additional Information"

    def __str__(self):
        return f"Additional information - {self.college.name}"


class CollegeAdditionalGallery(models.Model):
    information = models.ForeignKey(CollegeAdditionalInformation, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(upload_to="college_additional_gallery/")
    caption = models.CharField(max_length=180, blank=True)

    class Meta:
        verbose_name = "College Gallery Image"
        verbose_name_plural = "College Gallery Images"


class CourseAdditionalInformation(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name="additional_information")
    overview = models.TextField(blank=True, help_text="Additional text shown on the course detail page.")
    campus_tour_url = models.URLField("Campus Tours", blank=True, help_text="Campus tour video or virtual campus tour URL relevant to this course.")
    placement = models.TextField(blank=True, help_text="Career/placement details, recruiters and package information.")
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Course Additional Information"
        verbose_name_plural = "Course Additional Information"

    def __str__(self):
        return f"Additional information - {self.course.name}"


class CourseAdditionalGallery(models.Model):
    information = models.ForeignKey(CourseAdditionalInformation, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(upload_to="course_additional_gallery/")
    caption = models.CharField(max_length=180, blank=True)

    class Meta:
        verbose_name = "Course Gallery Image"
        verbose_name_plural = "Course Gallery Images"
