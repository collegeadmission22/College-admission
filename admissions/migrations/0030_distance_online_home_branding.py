from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [("admissions", "0029_college_country")]
    operations = [
        migrations.CreateModel(
            name="DistanceOnlineEducation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=180)),
                ("short_description", models.CharField(blank=True, max_length=220)),
                ("description", models.TextField(blank=True, verbose_name="Career path")),
                ("motivation", models.CharField(blank=True, max_length=180)),
                ("image", models.ImageField(blank=True, null=True, upload_to="distance_online/")),
                ("seo_title", models.CharField(blank=True, max_length=180)),
                ("seo_description", models.CharField(blank=True, max_length=320)),
                ("seo_keywords", models.TextField(blank=True)),
                ("seo_slug", models.SlugField(blank=True, db_index=True, max_length=220)),
                ("featured", models.BooleanField(default=False)),
                ("active", models.BooleanField(default=True)),
                ("categories", models.ManyToManyField(blank=True, related_name="distance_online_programmes", to="admissions.collegecategory")),
                ("country", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="distance_online_programmes", to="admissions.countrymaster")),
                ("state", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="distance_online_programmes", to="admissions.statemaster")),
                ("university", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="distance_online_programmes", to="admissions.universitymaster")),
            ],
            options={"verbose_name": "Distance / Online Education", "verbose_name_plural": "Distance / Online Education", "ordering": ("name",)},
        ),
        migrations.AddField(model_name="lead", name="preferred_distance_online", field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="leads", to="admissions.distanceonlineeducation", verbose_name="Distance / Online Education")),
        migrations.AddField(model_name="sitesettings", name="home_logo", field=models.ImageField(blank=True, help_text="Optional College Admission logo displayed on the home page.", null=True, upload_to="branding/")),
    ]
