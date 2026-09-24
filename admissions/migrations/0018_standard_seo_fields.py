from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("admissions", "0017_career_path_labels")]
    operations = [
        migrations.AddField(model_name="course", name="seo_keywords", field=models.TextField(blank=True, help_text="Comma-separated SEO keywords.")),
        migrations.AddField(model_name="course", name="seo_slug", field=models.SlugField(blank=True, db_index=True, help_text="SEO-friendly URL slug.", max_length=220)),
        migrations.AddField(model_name="college", name="seo_keywords", field=models.TextField(blank=True, help_text="Comma-separated SEO keywords.")),
        migrations.AddField(model_name="college", name="seo_slug", field=models.SlugField(blank=True, db_index=True, help_text="SEO-friendly URL slug.", max_length=220)),
        migrations.AddField(model_name="onlinecourse", name="seo_keywords", field=models.TextField(blank=True, help_text="Comma-separated SEO keywords.")),
        migrations.AddField(model_name="onlinecourse", name="seo_slug", field=models.SlugField(blank=True, db_index=True, help_text="SEO-friendly URL slug.", max_length=220)),
    ]
