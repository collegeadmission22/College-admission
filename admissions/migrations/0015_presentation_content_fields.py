from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("admissions", "0014_lead_document")]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="career_description",
            field=models.TextField("Description", blank=True),
        ),
        migrations.AddField(
            model_name="college",
            name="short_description",
            field=models.CharField(blank=True, help_text="Short card summary for the college.", max_length=220),
        ),
        migrations.AddField(
            model_name="college",
            name="motivation",
            field=models.CharField(blank=True, help_text="Motivational line shown on the college card/page.", max_length=220),
        ),
        migrations.AlterField(
            model_name="college",
            name="description",
            field=models.TextField(blank=True, help_text="Detailed college presentation / overview."),
        ),
        migrations.AddField(
            model_name="onlinecourse",
            name="short_description",
            field=models.CharField(blank=True, help_text="Short card summary for the online course.", max_length=220),
        ),
        migrations.AddField(
            model_name="onlinecourse",
            name="motivation",
            field=models.CharField(blank=True, help_text="Motivational line shown on the online course card/page.", max_length=220),
        ),
        migrations.AlterField(
            model_name="onlinecourse",
            name="description",
            field=models.TextField(blank=True, help_text="Detailed online course presentation / overview."),
        ),
    ]
