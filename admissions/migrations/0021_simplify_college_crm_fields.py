from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("admissions", "0020_simplified_college_categories")]
    operations = [
        migrations.AlterField(
            model_name="college",
            name="university",
            field=models.CharField(max_length=120, verbose_name="University Name"),
        ),
        migrations.AlterField(
            model_name="college",
            name="college_type",
            field=models.CharField(
                choices=[
                    ("Medical", "Medical Colleges"),
                    ("Management", "Management Colleges"),
                    ("Law", "Law Colleges"),
                    ("Engineering", "Engineering Colleges"),
                    ("Media", "Media Colleges"),
                    ("International", "International Colleges"),
                ],
                default="Engineering",
                max_length=30,
                verbose_name="College Category",
            ),
        ),
        migrations.AlterField(
            model_name="college",
            name="state",
            field=models.CharField(default="Delhi", max_length=80, verbose_name="State"),
        ),
    ]
