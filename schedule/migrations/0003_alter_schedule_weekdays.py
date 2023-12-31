# Generated by Django 4.2.2 on 2023-07-20 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("schedule", "0002_alter_schedule_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="schedule",
            name="weekdays",
            field=models.CharField(
                choices=[
                    ("monday", "Понедельник"),
                    ("tuesday", "Вторник"),
                    ("wednesday", "Среда"),
                    ("thursday", "Четверг"),
                    ("friday", "Пятница"),
                    ("saturday", "Суббота"),
                    ("sunday", "Воскресенье"),
                ],
                default="monday",
                max_length=15,
            ),
        ),
    ]
