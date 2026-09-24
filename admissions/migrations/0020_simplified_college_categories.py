from django.db import migrations

def seed_categories(apps, schema_editor):
    Category = apps.get_model('admissions', 'CollegeCategory')
    for name, slug in [
        ('Engineering College','engineering-college'),
        ('Management College','management-college'),
        ('Law College','law-college'),
        ('Medical College','medical-college'),
        ('Online College','online-college'),
    ]:
        Category.objects.get_or_create(slug=slug, defaults={'name': name})

class Migration(migrations.Migration):
    dependencies = [('admissions', '0019_remove_college_logo')]
    operations = [migrations.RunPython(seed_categories, migrations.RunPython.noop)]
