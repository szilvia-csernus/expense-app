# Generated by Django 4.2.9 on 2024-02-10 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0003_alter_claimscounter_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ClaimsCounter',
        ),
    ]
