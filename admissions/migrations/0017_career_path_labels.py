from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("admissions", "0016_college_categories")]
    operations = [
        migrations.AlterField(model_name="course", name="career_description", field=models.TextField("Career path", blank=True)),
        migrations.AlterField(model_name="college", name="description", field=models.TextField("Career path", blank=True, help_text="Career opportunities and professional pathways for students.")),
        migrations.AlterField(model_name="onlinecourse", name="description", field=models.TextField("Career path", blank=True, help_text="Career opportunities and professional pathways after this online course.")),
    ]
