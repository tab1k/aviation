# Generated by Django 4.2.2 on 2023-07-23 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("essays", "0004_essaysubmission_delete_essayresult"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="essay",
            options={"verbose_name": "Тема эссе", "verbose_name_plural": "Темы эссе"},
        ),
        migrations.RemoveField(
            model_name="essay",
            name="files",
        ),
        migrations.RemoveField(
            model_name="essay",
            name="user",
        ),
        migrations.AddField(
            model_name="essay",
            name="description",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AddField(
            model_name="essay",
            name="photo",
            field=models.ImageField(blank=True, null=True, upload_to="essay_photos/"),
        ),
        migrations.AlterField(
            model_name="essay",
            name="text",
            field=models.CharField(max_length=255),
        ),
    ]