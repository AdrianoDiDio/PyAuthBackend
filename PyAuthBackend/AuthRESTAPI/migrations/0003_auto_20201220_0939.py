# Generated by Django 3.1.4 on 2020-12-20 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AuthRESTAPI', '0002_auto_20201215_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='biometricToken',
        ),
        migrations.RemoveField(
            model_name='user',
            name='biometricTokenExp',
        ),
        migrations.RemoveField(
            model_name='user',
            name='biometricTokenIAt',
        ),
    ]
