# Generated by Django 4.2.2 on 2024-06-08 13:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0022_alter_course_students"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="image",
            field=models.ImageField(upload_to="course_images"),
        ),
    ]
