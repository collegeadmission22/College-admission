from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("admissions", "0018_standard_seo_fields")]
    operations = [migrations.RemoveField(model_name="college", name="logo")]
