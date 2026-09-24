from django.db import migrations, models


def seed_categories(apps, schema_editor):
    CollegeCategory = apps.get_model("admissions", "CollegeCategory")
    for name, slug in [
        ("Engineering", "engineering"),
        ("Management", "management"),
        ("Law", "law"),
        ("Pharmacy", "pharmacy"),
        ("Medical", "medical"),
        ("Computer Applications", "computer-applications"),
        ("Commerce", "commerce"),
        ("Media & Journalism", "media-journalism"),
        ("Education", "education"),
        ("Other", "other"),
    ]:
        CollegeCategory.objects.get_or_create(name=name, defaults={"slug": slug})


class Migration(migrations.Migration):
    dependencies = [("admissions", "0015_presentation_content_fields")]
    operations = [
        migrations.CreateModel(
            name="CollegeCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True)),
                ("slug", models.SlugField(max_length=60, unique=True)),
            ],
            options={"verbose_name_plural": "College categories", "ordering": ("name",)},
        ),
        migrations.AddField(
            model_name="college",
            name="categories",
            field=models.ManyToManyField(blank=True, help_text="Select one or more: Engineering, Management, Law, Pharmacy, Medical, etc.", related_name="colleges", to="admissions.collegecategory"),
        ),
        migrations.RunPython(seed_categories, migrations.RunPython.noop),
    ]
