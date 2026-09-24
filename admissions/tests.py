from django.contrib.auth.models import User
from django.test import Client, TestCase, override_settings
from django.core import mail
from django.core.management import call_command
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from datetime import timedelta
import hashlib, io, tempfile, zipfile
from PIL import Image

from .forms import LeadForm
from .bulk_data import process_bulk_rows, read_image_zip
from .models import BulkDataBatch, CRMApiKey, College, Course, FollowUp, Lead, NurtureLog, OnlineCourse, UserProfile
from .views import process_lead_rows, scoped_leads


class CRMWorkflowTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user("manager", password="pass", is_staff=True)
        self.agent = User.objects.create_user("agent", password="pass")
        UserProfile.objects.create(user=self.agent, role="Agent")

    def test_mobile_is_normalised_and_unique(self):
        Lead.objects.create(name="First", phone="+91 98765 43210")
        self.assertEqual(Lead.objects.get().phone, "9876543210")
        form = LeadForm({"name":"Updated", "phone":"98765-43210", "email":"", "city":"Delhi", "course":"", "preferred_college":"", "score":"", "consent":"on"})
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.assertEqual(Lead.objects.count(), 1)
        self.assertEqual(Lead.objects.get().name, "Updated")

    def test_bulk_import_updates_duplicate_and_assigns(self):
        Lead.objects.create(name="Old", phone="9999999999")
        rows = [{"Student Name":"New Name", "Mobile Number":"9999999999", "City":"Delhi"}, {"Student Name":"Second", "Mobile Number":"8888888888", "City":"Noida"}]
        batch = process_lead_rows(rows, "test.csv", self.staff, self.agent, "Other")
        self.assertEqual((batch.created_count, batch.updated_count, batch.rejected_count), (1, 1, 0))
        self.assertEqual(Lead.objects.get(phone="8888888888").assigned_to, self.agent)

    def test_bulk_data_creates_and_updates_catalogues_with_audit(self):
        rows = [{"Course Name":"B.Tech AI", "Category":"Engineering", "Level":"UG", "Duration":"4 Years"}]
        first = process_bulk_rows("courses", rows, "courses.csv", self.staff, "upsert")
        self.assertEqual((first.created_count, first.rejected_count), (1, 0))
        rows[0]["Duration"] = "Four Years"
        second = process_bulk_rows("courses", rows, "courses.csv", self.staff, "upsert")
        self.assertEqual(second.updated_count, 1)
        self.assertEqual(Course.objects.get(name="B.Tech AI").duration, "Four Years")
        self.assertEqual(BulkDataBatch.objects.count(), 2)

    def test_bulk_medical_college_and_online_course(self):
        Course.objects.create(name="MBBS", category="Medical")
        medical = process_bulk_rows("medical_colleges", [{"College Name":"Medical One", "University":"Health University", "State":"Delhi", "Courses":"MBBS", "Active":"Yes"}], "medical.xlsx", self.staff)
        online = process_bulk_rows("online_courses", [{"Title":"Online BBA", "Category":"Management", "Description":"Flexible programme", "Active":"Yes"}], "online.csv", self.staff)
        self.assertEqual((medical.created_count, online.created_count), (1, 1))
        self.assertEqual(College.objects.get(name="Medical One").college_type, "Medical")
        self.assertTrue(OnlineCourse.objects.get(title="Online BBA").active)

    def test_bulk_data_rejects_duplicate_rows_and_is_admin_staff_only(self):
        rows = [{"Course Name":"BCA", "Category":"Computer Applications"}, {"Course Name":"bca", "Category":"Computer Applications"}]
        batch = process_bulk_rows("courses", rows, "duplicate.csv", self.staff)
        self.assertEqual((batch.created_count, batch.rejected_count), (1, 1))
        client = Client(HTTP_HOST="localhost"); client.force_login(self.agent)
        self.assertEqual(client.get("/crm/bulk-data/").status_code, 403)
        client.force_login(self.staff)
        self.assertEqual(client.get("/crm/bulk-data/").status_code, 200)
        self.assertEqual(client.get("/crm/bulk-data/courses/template/xlsx/").status_code, 200)
        self.assertEqual(client.get("/crm/bulk-data/courses/export/csv/").status_code, 200)

    def test_bulk_course_image_zip_is_matched_and_saved(self):
        image_bytes = io.BytesIO(); Image.new("RGB", (8, 8), "blue").save(image_bytes, format="PNG")
        zip_bytes = io.BytesIO()
        with zipfile.ZipFile(zip_bytes, "w") as archive: archive.writestr("course-ai.png", image_bytes.getvalue())
        upload = SimpleUploadedFile("images.zip", zip_bytes.getvalue(), content_type="application/zip")
        images = read_image_zip(upload)
        with tempfile.TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            batch = process_bulk_rows("courses", [{"Course Name":"AI Course", "Category":"Engineering", "Image Filename":"course-ai.png"}], "courses.csv", self.staff, images=images)
            course = Course.objects.get(name="AI Course")
            self.assertTrue(course.image.name.endswith("course-ai.png"))
            self.assertEqual(batch.imported_image_count, 1)

    def test_agent_only_sees_own_leads(self):
        own = Lead.objects.create(name="Own", phone="7777777777", assigned_to=self.agent)
        Lead.objects.create(name="Other", phone="6666666666")
        self.assertEqual(list(scoped_leads(self.agent)), [own])

    def test_role_aware_crm_pages_and_exports(self):
        client = Client(HTTP_HOST="localhost"); client.force_login(self.staff)
        for path in ["/crm/", "/crm/calendar/", "/crm/reports/", "/crm/import/", "/crm/export/csv/", "/crm/export/xlsx/", "/crm/export/pdf/"]:
            self.assertEqual(client.get(path).status_code, 200)

    def test_nurturing_report_filters_and_followup_stages(self):
        delhi = Lead.objects.create(name="Delhi Hot", phone="9111111111", city="Delhi", source="Google Ads", status="Hot", call_outcome="Connected", assigned_to=self.agent)
        Lead.objects.create(name="Noida Lead", phone="9222222222", city="Noida", source="Website", status="New Enquiry")
        FollowUp.objects.create(lead=delhi, due_at=timezone.now()-timedelta(days=1), note="Overdue call", created_by=self.staff)
        FollowUp.objects.create(lead=delhi, due_at=timezone.now()-timedelta(days=2), note="Finished call", completed=True, completed_at=timezone.now(), created_by=self.staff)
        client = Client(HTTP_HOST="localhost"); client.force_login(self.staff)
        response = client.get("/crm/reports/?city=Delhi&source=Google+Ads")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total"], 1)
        self.assertEqual(response.context["contact_rate"], 100.0)
        self.assertEqual(response.context["overdue"], 1)
        self.assertEqual(response.context["completed_followups"], 1)
        self.assertEqual(response.context["total_campaigns"], 0)
        self.assertContains(response, "Lead Nurturing Analysis")

    def test_day_one_nurturing_is_logged_once(self):
        lead=Lead.objects.create(name="Nurture",phone="9333333333",assigned_to=self.agent,consent=True)
        Lead.objects.filter(pk=lead.pk).update(created_at=timezone.now()-timedelta(days=1))
        call_command("run_lead_nurturing")
        self.assertTrue(NurtureLog.objects.filter(lead=lead,day=1).exists())
        self.assertTrue(FollowUp.objects.filter(lead=lead,note__icontains="welcome call").exists())
        call_command("run_lead_nurturing")
        self.assertEqual(NurtureLog.objects.filter(lead=lead,day=1).count(),1)

    def test_admin_api_key_creates_and_updates_by_mobile(self):
        raw = "ca_live_test-secret"
        CRMApiKey.objects.create(owner=self.agent, name="Test", prefix=raw[:16], key_hash=hashlib.sha256(raw.encode()).hexdigest(), created_by=self.staff)
        client = Client(HTTP_HOST="localhost")
        response = client.post("/api/v1/leads/", data='{"name":"API Student","mobile":"9555555555","city":"Delhi"}', content_type="application/json", HTTP_X_API_KEY=raw)
        self.assertEqual(response.status_code, 201)
        response = client.post("/api/v1/leads/", data='{"name":"Updated API Student","mobile":"9555555555"}', content_type="application/json", HTTP_X_API_KEY=raw)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.filter(phone="9555555555").count(), 1)

    def test_only_admin_can_open_authorisation_panels(self):
        client = Client(HTTP_HOST="localhost"); client.force_login(self.staff)
        self.assertEqual(client.get("/crm/consultants/").status_code, 403)
        self.staff.is_superuser = True; self.staff.save(); client.force_login(self.staff)
        self.assertEqual(client.get("/crm/consultants/").status_code, 200)
        self.assertEqual(client.get("/crm/api-keys/").status_code, 200)
        self.assertEqual(client.get("/crm/integrations/").status_code, 200)

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_due_followup_emails_assigned_user_once(self):
        self.agent.email = "agent@example.com"; self.agent.save()
        lead = Lead.objects.create(name="Reminder", phone="9444444444", assigned_to=self.agent)
        followup = FollowUp.objects.create(lead=lead, due_at=timezone.now()+timedelta(minutes=5), note="Call parent", reminder_minutes_before=10, created_by=self.staff)
        call_command("send_followup_reminders")
        followup.refresh_from_db()
        self.assertIsNotNone(followup.reminder_sent_at)
        self.assertEqual(len(mail.outbox), 1)
        call_command("send_followup_reminders")
        self.assertEqual(len(mail.outbox), 1)
