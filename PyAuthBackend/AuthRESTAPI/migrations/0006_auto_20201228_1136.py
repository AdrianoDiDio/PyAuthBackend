# Generated by Django 3.1.4 on 2020-12-28 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AuthRESTAPI', '0005_auto_20201227_1115'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='biometric_token',
            new_name='biometricToken',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='public_key',
            new_name='publicKey',
        ),
    ]
