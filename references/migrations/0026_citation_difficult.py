# Generated by Django 3.2.9 on 2023-04-19 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0025_citation_citation_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='citation',
            name='difficult',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
