# Generated by Django 3.1.4 on 2020-12-31 21:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20201221_1131'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('browser', models.CharField(blank=True, max_length=255, null=True, verbose_name='Browser')),
                ('os', models.CharField(blank=True, max_length=255, null=True, verbose_name='Browser')),
                ('ip', models.CharField(blank=True, max_length=255, null=True, verbose_name='Browser')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
