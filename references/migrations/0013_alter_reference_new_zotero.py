# Generated by Django 3.2.9 on 2021-12-13 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0012_alter_reference__pass'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='new_zotero',
            field=models.CharField(blank=True, default='ALi', max_length=300, null=True),
        ),
    ]
