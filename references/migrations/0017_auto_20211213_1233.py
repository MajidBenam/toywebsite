# Generated by Django 3.2.9 on 2021-12-13 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0016_auto_20211213_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='_pass',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='reference',
            name='_reviewed',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
