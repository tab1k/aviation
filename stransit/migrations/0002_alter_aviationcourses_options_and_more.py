# Generated by Django 4.2.2 on 2023-08-02 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stransit", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="aviationcourses",
            options={
                "verbose_name": "Авиционный курс",
                "verbose_name_plural": "Авиационные курсы",
            },
        ),
        migrations.AlterModelOptions(
            name="industrialcourses",
            options={
                "verbose_name": "Промышленный курс",
                "verbose_name_plural": "Промышленные курсы",
            },
        ),
        migrations.AlterModelOptions(
            name="onlinecourses",
            options={
                "verbose_name": "Онлайн курс",
                "verbose_name_plural": "Онлайн курсы",
            },
        ),
        migrations.AlterField(
            model_name="aviationcourses",
            name="about_course",
            field=models.TextField(max_length=300, verbose_name="О курсе"),
        ),
        migrations.AlterField(
            model_name="aviationcourses",
            name="photo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="stransit_course_images",
                verbose_name="Фото",
            ),
        ),
        migrations.AlterField(
            model_name="aviationcourses",
            name="title",
            field=models.CharField(max_length=255, verbose_name="Название курса"),
        ),
        migrations.AlterField(
            model_name="aviationcourses",
            name="type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("online", "Онлайн курс"),
                    ("industrial", "Промышленный курс"),
                    ("aviation", "Авиационный курс"),
                ],
                default="offline",
                max_length=10,
                null=True,
                verbose_name="Формат обучения",
            ),
        ),
        migrations.AlterField(
            model_name="industrialcourses",
            name="about_course",
            field=models.TextField(max_length=300, verbose_name="О курсе"),
        ),
        migrations.AlterField(
            model_name="industrialcourses",
            name="photo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="stransit_course_images",
                verbose_name="Фото",
            ),
        ),
        migrations.AlterField(
            model_name="industrialcourses",
            name="title",
            field=models.CharField(max_length=255, verbose_name="Название курса"),
        ),
        migrations.AlterField(
            model_name="industrialcourses",
            name="type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("online", "Онлайн курс"),
                    ("industrial", "Промышленный курс"),
                    ("aviation", "Авиационный курс"),
                ],
                default="offline",
                max_length=10,
                null=True,
                verbose_name="Формат обучения",
            ),
        ),
        migrations.AlterField(
            model_name="onlinecourses",
            name="about_course",
            field=models.TextField(max_length=300, verbose_name="О курсе"),
        ),
        migrations.AlterField(
            model_name="onlinecourses",
            name="photo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="stransit_course_images",
                verbose_name="Фото",
            ),
        ),
        migrations.AlterField(
            model_name="onlinecourses",
            name="title",
            field=models.CharField(max_length=255, verbose_name="Название курса"),
        ),
        migrations.AlterField(
            model_name="onlinecourses",
            name="type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("online", "Онлайн курс"),
                    ("industrial", "Промышленный курс"),
                    ("aviation", "Авиационный курс"),
                ],
                default="offline",
                max_length=10,
                null=True,
                verbose_name="Формат обучения",
            ),
        ),
    ]