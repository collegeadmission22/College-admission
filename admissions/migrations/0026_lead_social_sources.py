from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("admissions", "0025_campus_tours_cleanup")]
    operations = [
        migrations.AlterField(
            model_name="lead",
            name="source",
            field=models.CharField(choices=[(x,x) for x in ["Website","Google Ads","Facebook","Facebook Messenger","Instagram","Instagram Messenger","WhatsApp","WhatsApp Chatbot","AI Chatbot","Contact Form","Phone Call","Walk-in","Referral","YouTube","LinkedIn","Other"]], default="Website", max_length=30),
        ),
    ]
