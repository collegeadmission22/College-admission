from django.urls import path
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path("", views.home, name="home"), path("health/", views.health, name="health"), path("about/", views.about, name="about"), path("contact/", views.contact, name="contact"),
    path("courses/", views.courses_page, name="courses_page"), path("courses/<int:pk>/", views.course_detail, name="course_detail"), path("colleges/", views.colleges_page, name="colleges_page"), path("colleges/<int:pk>/", views.college_detail, name="college_detail"), path("medical-colleges/", views.medical_colleges, name="medical_colleges"), path("online-courses/", views.online_courses, name="online_courses"), path("quick-apply/", views.quick_apply, name="quick_apply"),
    path("social/<str:platform>/", views.social_redirect, name="social_redirect"), path("api/chatbot/", views.chatbot, name="chatbot"),
    path("student/register/", views.student_signup, name="student_signup"), path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("crm/", views.dashboard, name="dashboard"), path("crm/leads/add/", views.add_own_lead, name="add_own_lead"), path("crm/pipeline/", views.admission_pipeline, name="admission_pipeline"), path("crm/module/<str:module>/", views.module_dashboard, name="module_dashboard"), path("crm/leads/<int:pk>/", views.lead_detail, name="lead_detail"),
    path("crm/import/", views.import_leads, name="import_leads"), path("crm/export/<str:file_format>/", views.export_leads, name="export_leads"),
    path("crm/calendar/", views.followup_calendar, name="followup_calendar"), path("crm/consultants/", views.consultant_panel, name="consultant_panel"),
    path("crm/api-keys/", views.api_key_panel, name="api_key_panel"), path("crm/api-keys/<int:pk>/revoke/", views.revoke_api_key, name="revoke_api_key"),
    path("crm/followups/<int:pk>/complete/", views.complete_followup, name="complete_followup"), path("crm/integrations/", views.integration_settings, name="integration_settings"),
    path("crm/reports/", views.reports_dashboard, name="reports_dashboard"),
    path("crm/bulk-data/", views.bulk_data_manager, name="bulk_data_manager"),
    path("crm/bulk-data/<str:dataset>/template/<str:file_format>/", views.bulk_data_template, name="bulk_data_template"),
    path("crm/bulk-data/<str:dataset>/export/<str:file_format>/", views.bulk_data_export, name="bulk_data_export"),
    path("crm/bulk-data/batches/<int:pk>/errors/", views.bulk_data_errors, name="bulk_data_errors"),
    path("api/v1/leads/", views.api_leads, name="api_leads")]
