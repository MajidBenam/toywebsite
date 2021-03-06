# Generated by Django 3.2.9 on 2021-12-02 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_ref', models.TextField()),
                ('polity', models.CharField(max_length=20)),
                ('creator', models.CharField(blank=True, default='Majid', max_length=60, null=True)),
                ('year', models.IntegerField(blank=True)),
                ('title', models.CharField(blank=True, max_length=300)),
                ('certainty', models.IntegerField(default=-1)),
                ('gs_stars', models.IntegerField()),
                ('final_check', models.BooleanField()),
                ('new_zotero', models.URLField()),
            ],
        ),
    ]
