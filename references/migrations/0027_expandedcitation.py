# Generated by Django 3.2.9 on 2023-06-09 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0026_citation_difficult'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpandedCitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expanded_citation_text', models.TextField()),
                ('expanded_polity', models.CharField(max_length=20)),
                ('expanded_site', models.CharField(blank=True, choices=[('wiki', 'Seshat.info'), ('browser', 'seshatdatabank.info')], max_length=8, null=True)),
                ('expanded_citation_number', models.IntegerField(blank=True, default=0, null=True)),
                ('citation_on_toy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ref1', to='references.citation')),
                ('citation_on_toy_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ref2', to='references.citation')),
                ('citation_on_toy_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ref3', to='references.citation')),
            ],
            options={
                'db_table': 'expandedcitations',
            },
        ),
    ]
