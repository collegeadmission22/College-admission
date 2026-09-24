from django.db import migrations, models
import django.db.models.deletion


def copy_college_master_data(apps, schema_editor):
    College = apps.get_model('admissions', 'College')
    Country = apps.get_model('admissions', 'CountryMaster')
    State = apps.get_model('admissions', 'StateMaster')
    University = apps.get_model('admissions', 'UniversityMaster')
    india, _ = Country.objects.get_or_create(name='India', defaults={'active': True})
    for c in College.objects.all():
        state_name = (c.state_text or 'Delhi').strip()
        st, _ = State.objects.get_or_create(country=india, name=state_name, defaults={'active': True})
        uni_name = (c.university_text or '').strip()
        uni = None
        if uni_name:
            uni, _ = University.objects.get_or_create(name=uni_name, defaults={'state': st, 'active': True})
        c.state_master = st
        c.university_master = uni
        c.save(update_fields=['state_master', 'university_master'])

class Migration(migrations.Migration):
    dependencies = [('admissions', '0022_admission_master_data')]
    operations = [
        migrations.RenameField(model_name='college', old_name='university', new_name='university_text'),
        migrations.RenameField(model_name='college', old_name='state', new_name='state_text'),
        migrations.AddField(model_name='college', name='university_master', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='colleges', to='admissions.universitymaster', verbose_name='University Name')),
        migrations.AddField(model_name='college', name='state_master', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='colleges', to='admissions.statemaster', verbose_name='State')),
        migrations.RunPython(copy_college_master_data, migrations.RunPython.noop),
        migrations.RemoveField(model_name='college', name='university_text'),
        migrations.RemoveField(model_name='college', name='state_text'),
        migrations.RenameField(model_name='college', old_name='university_master', new_name='university'),
        migrations.RenameField(model_name='college', old_name='state_master', new_name='state'),
    ]
