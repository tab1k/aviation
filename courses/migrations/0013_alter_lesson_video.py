# Generated by Django 4.2.2 on 2023-08-04 12:04

from django.db import migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0012_lesson_learn_documentation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="video",
            field=embed_video.fields.EmbedVideoField(blank=True, null=True),
        ),
    ]