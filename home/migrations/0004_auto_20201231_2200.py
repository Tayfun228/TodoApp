# Generated by Django 3.1.4 on 2020-12-31 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20201231_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='celery_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Celery ID'),
        ),
    ]
