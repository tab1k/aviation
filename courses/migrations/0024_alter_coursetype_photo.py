# Generated by Django 4.2.2 on 2024-06-08 14:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0023_alter_course_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coursetype",
            name="photo",
            field=models.ImageField(upload_to="course_type_images"),
        ),
    ]