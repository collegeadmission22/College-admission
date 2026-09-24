from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("admissions", "0024_additional_information_pages")]
    operations = [
        migrations.RenameField(model_name="collegeadditionalinformation", old_name="video_url", new_name="campus_tour_url"),
        migrations.AlterField(model_name="collegeadditionalinformation", name="campus_tour_url", field=models.URLField(blank=True, help_text="Campus tour video or virtual campus tour URL.", verbose_name="Campus Tours")),
        migrations.RemoveField(model_name="collegeadditionalinformation", name="brochure"),
        migrations.RemoveField(model_name="collegeadditionalinformation", name="ranking"),
        migrations.RenameField(model_name="courseadditionalinformation", old_name="video_url", new_name="campus_tour_url"),
        migrations.AlterField(model_name="courseadditionalinformation", name="campus_tour_url", field=models.URLField(blank=True, help_text="Campus tour video or virtual campus tour URL relevant to this course.", verbose_name="Campus Tours")),
        migrations.RemoveField(model_name="courseadditionalinformation", name="brochure"),
        migrations.RemoveField(model_name="courseadditionalinformation", name="ranking"),
    ]
