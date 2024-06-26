# Generated by Django 5.0.3 on 2024-03-30 14:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_deviceassignment'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignmentLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkout_date', models.DateTimeField()),
                ('checkout_note', models.TextField(blank=True, null=True)),
                ('return_date', models.DateTimeField(blank=True, null=True)),
                ('return_note', models.TextField(blank=True, null=True)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.deviceassignment')),
            ],
        ),
    ]
