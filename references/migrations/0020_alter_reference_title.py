# Generated by Django 3.2.9 on 2021-12-15 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0019_alter_reference_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='title',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
