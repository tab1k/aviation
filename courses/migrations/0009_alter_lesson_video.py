# Generated by Django 4.2.2 on 2023-07-13 01:27

from django.db import migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0008_course_students"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="video",
            field=embed_video.fields.EmbedVideoField(),
        ),
    ]
