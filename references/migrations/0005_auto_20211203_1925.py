# Generated by Django 3.2.9 on 2021-12-03 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0004_auto_20211203_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='reference',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
