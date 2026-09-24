from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [("admissions", "0021_simplify_college_crm_fields")]
    operations = [
        migrations.CreateModel(name="CountryMaster", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=100, unique=True)), ("active", models.BooleanField(default=True))], options={"verbose_name":"Country","verbose_name_plural":"Countries","ordering":("name",)}),
        migrations.CreateModel(name="CourseCategoryMaster", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=100, unique=True)), ("active", models.BooleanField(default=True))], options={"verbose_name":"Course Category","verbose_name_plural":"Course Categories","ordering":("name",)}),
        migrations.CreateModel(name="StateMaster", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=100)), ("active", models.BooleanField(default=True)), ("country", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="states", to="admissions.countrymaster"))], options={"verbose_name":"State","verbose_name_plural":"States","ordering":("country__name","name")}),
        migrations.AddConstraint(model_name="statemaster", constraint=models.UniqueConstraint(fields=("country","name"), name="unique_state_per_country")),
        migrations.CreateModel(name="UniversityMaster", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=180, unique=True)), ("active", models.BooleanField(default=True)), ("state", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="universities", to="admissions.statemaster"))], options={"verbose_name":"University Name","verbose_name_plural":"University Names","ordering":("name",)}),
    ]
