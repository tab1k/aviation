# Generated by Django 4.2.2 on 2023-09-19 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stransit", "0007_alter_contact_phone_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="phone_number",
            field=models.BigIntegerField(null=True),
        ),
    ]
