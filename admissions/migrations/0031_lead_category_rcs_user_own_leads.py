from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("admissions", "0030_distance_online_home_branding")]
    operations = [
        migrations.AddField(model_name="lead", name="lead_category", field=models.CharField(choices=[("Hot","Hot"),("Warm","Warm"),("Cold","Cold"),("Fresh","Fresh"),("Follow-up","Follow-up"),("Admission Ready","Admission Ready"),("Converted","Converted"),("Lost","Lost")], db_index=True, default="Fresh", help_text="Lead priority/category used by counsellors for nurturing and conversion.", max_length=30)),
        migrations.AddField(model_name="userprofile", name="can_add_own_leads", field=models.BooleanField(default=True, help_text="Allow this user to add leads to their own CRM panel.")),
        migrations.AlterField(model_name="communication", name="channel", field=models.CharField(choices=[("Email","Email"),("WhatsApp","WhatsApp"),("SMS","SMS"),("RCS","RCS")], max_length=20)),
        migrations.AlterField(model_name="communicationtemplate", name="channel", field=models.CharField(choices=[("Email","Email"),("WhatsApp","WhatsApp"),("SMS","SMS"),("RCS","RCS")], max_length=20)),
    ]
