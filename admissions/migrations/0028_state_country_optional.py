from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("admissions", "0027_multi_categories_college_course")]

    operations = [
        migrations.AlterField(
            model_name="statemaster",
            name="country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="states",
                to="admissions.countrymaster",
            ),
        ),
    ]
