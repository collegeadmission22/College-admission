from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [("admissions", "0011_bulkdatabatch_imported_image_count")]
    operations = [
        migrations.AddField(model_name="course", name="specialization", field=models.CharField(blank=True, max_length=160)),
        migrations.AddField(model_name="course", name="eligibility", field=models.TextField(blank=True)),
        migrations.AddField(model_name="course", name="entrance_exam", field=models.CharField(blank=True, max_length=160)),
        migrations.AddField(model_name="course", name="annual_fee", field=models.CharField(blank=True, max_length=80)),
        migrations.AddField(model_name="course", name="total_fee", field=models.CharField(blank=True, max_length=80)),
        migrations.AddField(model_name="course", name="seats", field=models.PositiveIntegerField(blank=True, null=True)),
        migrations.AddField(model_name="course", name="brochure_url", field=models.URLField(blank=True)),
        migrations.AddField(model_name="course", name="seo_title", field=models.CharField(blank=True, max_length=180)),
        migrations.AddField(model_name="course", name="seo_description", field=models.CharField(blank=True, max_length=320)),
        *[migrations.AddField(model_name="college", name=n, field=f) for n,f in [
            ("address",models.TextField(blank=True)),("website",models.URLField(blank=True)),("phone",models.CharField(blank=True,max_length=40)),("email",models.EmailField(blank=True,max_length=254)),("approvals",models.CharField(blank=True,max_length=240)),("ranking",models.CharField(blank=True,max_length=240)),("accreditation",models.CharField(blank=True,max_length=160)),("average_package",models.CharField(blank=True,max_length=80)),("highest_package",models.CharField(blank=True,max_length=80)),("hostel",models.CharField(blank=True,max_length=160)),("admission_deadline",models.CharField(blank=True,max_length=120)),("scholarship",models.TextField(blank=True)),("admission_mode",models.CharField(blank=True,max_length=160)),("brochure_url",models.URLField(blank=True)),("seo_title",models.CharField(blank=True,max_length=180)),("seo_description",models.CharField(blank=True,max_length=320))]],
        *[migrations.AddField(model_name="onlinecourse", name=n, field=f) for n,f in [
            ("eligibility",models.TextField(blank=True)),("accreditation",models.CharField(blank=True,max_length=180)),("exam_mode",models.CharField(blank=True,max_length=120)),("lms_details",models.TextField(blank=True)),("specialization",models.CharField(blank=True,max_length=180)),("application_url",models.URLField(blank=True)),("brochure_url",models.URLField(blank=True)),("seo_title",models.CharField(blank=True,max_length=180)),("seo_description",models.CharField(blank=True,max_length=320))]],
        migrations.CreateModel(name="CollegeImage", fields=[("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("image",models.ImageField(upload_to="college_gallery/")),("caption",models.CharField(blank=True,max_length=180)),("created_at",models.DateTimeField(auto_now_add=True)),("college",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="gallery_images",to="admissions.college"))]),
    ]
