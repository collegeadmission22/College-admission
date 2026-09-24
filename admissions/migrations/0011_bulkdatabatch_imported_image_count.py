from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("admissions", "0010_bulkdatabatch")]
    operations = [
        migrations.AddField(
            model_name="bulkdatabatch",
            name="imported_image_count",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
