# Generated by Django 3.2.9 on 2021-12-15 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0017_auto_20211213_1233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reference',
            name='_reviewed',
        ),
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
        migrations.AlterField(
            model_name='reference',
            name='new_zotero',
            field=models.CharField(blank=True, default='NO_ZOTERO', max_length=300, null=True),
        ),
    ]
