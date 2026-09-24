# Generated for bulk catalogue and lead import audit history.
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admissions", "0009_lead_class_10_percentage_lead_class_12_percentage_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name="BulkDataBatch",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("dataset", models.CharField(choices=[("leads", "Leads"), ("courses", "Courses"), ("colleges", "Colleges"), ("medical_colleges", "Medical Colleges"), ("online_courses", "Online Courses")], max_length=30)),
                ("mode", models.CharField(choices=[("create", "Create new only"), ("upsert", "Create and update")], default="upsert", max_length=10)),
                ("file_name", models.CharField(max_length=255)),
                ("total_rows", models.PositiveIntegerField(default=0)),
                ("created_count", models.PositiveIntegerField(default=0)),
                ("updated_count", models.PositiveIntegerField(default=0)),
                ("skipped_count", models.PositiveIntegerField(default=0)),
                ("rejected_count", models.PositiveIntegerField(default=0)),
                ("error_report", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("uploaded_by", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
