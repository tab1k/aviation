# Generated by Django 4.2.2 on 2023-08-28 20:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0017_alter_notification_options_lesson_course"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("comments", "0008_remove_comment_parent_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="curator",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments_curator",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Инструктор",
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="lesson",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="courses.lesson",
                verbose_name="Урок",
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="timestamp",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Время"
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
    ]