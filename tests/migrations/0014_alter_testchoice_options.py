# Generated by Django 4.2.2 on 2023-08-28 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tests", "0013_test_question_image_testchoice_choice_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="testchoice",
            options={
                "verbose_name": "Тестовый ответ",
                "verbose_name_plural": "Тестовые ответы",
            },
        ),
    ]
