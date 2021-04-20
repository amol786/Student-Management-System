# Generated by Django 2.2.8 on 2021-04-17 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('id', models.CharField(editable=False, max_length=200, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('registeration_num', models.CharField(max_length=100)),
                ('admission_date', models.CharField(max_length=200)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('created_dt', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('modify_dt', models.DateTimeField(auto_now=True, verbose_name='modified date')),
            ],
        ),
    ]