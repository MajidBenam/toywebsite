# Generated by Django 3.2.9 on 2021-12-13 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0010_auto_20211213_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='_reviewed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
