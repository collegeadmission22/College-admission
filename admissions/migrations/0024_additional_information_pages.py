from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [("admissions", "0023_college_master_dropdowns")]
    operations = [
        migrations.CreateModel(name="CollegeAdditionalInformation", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("overview", models.TextField(blank=True, help_text="Additional text shown on the college detail page.")),
            ("video_url", models.URLField(blank=True, help_text="YouTube or other public video URL.")),
            ("brochure", models.FileField(blank=True, null=True, upload_to="college_brochures/")),
            ("placement", models.TextField(blank=True, help_text="Placement details, recruiters and package information.")),
            ("ranking", models.TextField(blank=True, help_text="Ranking name, year, rank and source.", verbose_name="Rank / Ranking")),
            ("active", models.BooleanField(default=True)),
            ("college", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="additional_information", to="admissions.college")),
        ], options={"verbose_name":"College Additional Information","verbose_name_plural":"College Additional Information"}),
        migrations.CreateModel(name="CourseAdditionalInformation", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("overview", models.TextField(blank=True, help_text="Additional text shown on the course detail page.")),
            ("video_url", models.URLField(blank=True, help_text="YouTube or other public video URL.")),
            ("brochure", models.FileField(blank=True, null=True, upload_to="course_brochures/")),
            ("placement", models.TextField(blank=True, help_text="Career/placement details, recruiters and package information.")),
            ("ranking", models.TextField(blank=True, help_text="Ranking/accreditation information where applicable.", verbose_name="Rank / Ranking")),
            ("active", models.BooleanField(default=True)),
            ("course", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="additional_information", to="admissions.course")),
        ], options={"verbose_name":"Course Additional Information","verbose_name_plural":"Course Additional Information"}),
        migrations.CreateModel(name="CollegeAdditionalGallery", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("image", models.ImageField(upload_to="college_additional_gallery/")), ("caption", models.CharField(blank=True, max_length=180)),
            ("information", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="gallery", to="admissions.collegeadditionalinformation")),
        ], options={"verbose_name":"College Gallery Image","verbose_name_plural":"College Gallery Images"}),
        migrations.CreateModel(name="CourseAdditionalGallery", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("image", models.ImageField(upload_to="course_additional_gallery/")), ("caption", models.CharField(blank=True, max_length=180)),
            ("information", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="gallery", to="admissions.courseadditionalinformation")),
        ], options={"verbose_name":"Course Gallery Image","verbose_name_plural":"Course Gallery Images"}),
    ]
