# Generated by Django 5.1.4 on 2025-01-02 12:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0004_remove_location_related_present_location'),
        ('person', '0010_profile_burial_date_range_end_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marriage',
            name='divorce_circa',
        ),
        migrations.RemoveField(
            model_name='marriage',
            name='husband',
        ),
        migrations.RemoveField(
            model_name='marriage',
            name='marriage_circa',
        ),
        migrations.RemoveField(
            model_name='marriage',
            name='marriage_status',
        ),
        migrations.RemoveField(
            model_name='marriage',
            name='wife',
        ),
        migrations.AddField(
            model_name='marriage',
            name='divorce_date_type',
            field=models.CharField(choices=[('EXACT', 'Exact'), ('BEFORE', 'Before'), ('AFTER', 'After'), ('CIRCA', 'Circa'), ('BETWEEN', 'Between'), ('UNKNOWN', 'Unknown')], default='EXACT', max_length=16),
        ),
        migrations.AddField(
            model_name='marriage',
            name='marriage_date_type',
            field=models.CharField(choices=[('EXACT', 'Exact'), ('BEFORE', 'Before'), ('AFTER', 'After'), ('CIRCA', 'Circa'), ('BETWEEN', 'Between'), ('UNKNOWN', 'Unknown')], default='EXACT', max_length=16),
        ),
        migrations.AddField(
            model_name='marriage',
            name='relationship_status',
            field=models.CharField(choices=[('M', 'Married'), ('D', 'Divorced'), ('S', 'Separated'), ('U', 'Unknown')], default='M', max_length=1),
        ),
        migrations.AddField(
            model_name='marriage',
            name='spouse1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='marriages_as_spouse1', to='person.profile'),
        ),
        migrations.AddField(
            model_name='marriage',
            name='spouse2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='marriages_as_spouse2', to='person.profile'),
        ),
        migrations.AlterField(
            model_name='marriage',
            name='marriage_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='marriage_location', to='location.location'),
        ),
    ]
