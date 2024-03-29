# Generated by Django 4.2.9 on 2024-02-10 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Church',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=100)),
                ('long_name', models.CharField(blank=True, max_length=200, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos/')),
                ('claims_counter', models.IntegerField(default=0)),
                ('finance_contact_name', models.CharField(blank=True, max_length=200, null=True)),
                ('finance_email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
            options={
                'verbose_name_plural': 'Churches',
            },
        ),
        migrations.CreateModel(
            name='CostPurpose',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('cost_code', models.IntegerField(blank=True, null=True)),
                ('church', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cost_purposes', to='cost_centers.church')),
            ],
        ),
    ]
