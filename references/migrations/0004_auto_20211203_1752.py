# Generated by Django 3.2.9 on 2021-12-03 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0003_alter_reference_new_zotero'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reference',
            name='final_check',
        ),
        migrations.AddField(
            model_name='reference',
            name='_fail',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='reference',
            name='_pass',
            field=models.BooleanField(default=False),
        ),
    ]