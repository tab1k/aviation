# Generated by Django 4.2.2 on 2023-08-27 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comments", "0005_comment_timestamp"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="student_response",
            field=models.TextField(blank=True, null=True),
        ),
    ]
