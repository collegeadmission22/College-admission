from django.db import migrations, models


def copy_existing_categories(apps, schema_editor):
    Course = apps.get_model('admissions', 'Course')
    CollegeCategory = apps.get_model('admissions', 'CollegeCategory')
    CourseCategoryMaster = apps.get_model('admissions', 'CourseCategoryMaster')
    College = apps.get_model('admissions', 'College')

    # Preserve current College category values in the many-to-many master relation.
    for college in College.objects.all():
        if not college.categories.exists() and college.college_type:
            cat, _ = CollegeCategory.objects.get_or_create(
                name=college.college_type,
                defaults={'slug': college.college_type.lower().replace(' ', '-')[:60]},
            )
            college.categories.add(cat)

    # Preserve the existing Course.category value as a Course Category master entry.
    for course in Course.objects.all():
        if course.category:
            cc, _ = CourseCategoryMaster.objects.get_or_create(name=course.category)
            course.course_categories.add(cc)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [('admissions', '0026_lead_social_sources')]
    operations = [
        migrations.AddField(
            model_name='course',
            name='college_categories',
            field=models.ManyToManyField(blank=True, help_text='Select one or more college categories for this course.', related_name='courses_by_category', to='admissions.collegecategory', verbose_name='College Categories'),
        ),
        migrations.AddField(
            model_name='course',
            name='course_categories',
            field=models.ManyToManyField(blank=True, help_text='Select one or more course categories.', related_name='courses', to='admissions.coursecategorymaster', verbose_name='Course Categories'),
        ),
        migrations.RunPython(copy_existing_categories, noop_reverse),
    ]
