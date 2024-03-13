# Generated by Django 4.2.2 on 2024-03-13 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0020_course_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="module",
            name="course",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="modules",
                to="courses.course",
            ),
        ),
    ]
