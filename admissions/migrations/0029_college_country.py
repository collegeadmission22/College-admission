from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [("admissions", "0028_state_country_optional")]
    operations = [
        migrations.AddField(
            model_name="college",
            name="country",
            field=models.ForeignKey(blank=True, help_text="Optional. State and Country can be selected independently.", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="colleges", to="admissions.countrymaster", verbose_name="Country"),
        ),
    ]
