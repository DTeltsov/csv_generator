# Generated by Django 3.0.6 on 2022-04-23 15:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Column_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('has_range', models.BooleanField(verbose_name='Has range')),
            ],
        ),
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('column_separator', models.CharField(choices=[(',', 'Comma'), (';', 'Semicolon'), ('|', 'Pipe')], default=',', max_length=2, verbose_name='Separator')),
                ('string_character', models.CharField(choices=[("'", 'Quotes'), ('"', 'Double quotes')], default='"', max_length=2, verbose_name='Character')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Modification date')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schema', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rows_number', models.IntegerField(verbose_name='Number of rows')),
                ('state', models.CharField(choices=[('p', 'Processing'), ('r', 'Ready')], default='p', max_length=2, verbose_name='State')),
                ('date_created', models.DateTimeField(auto_now=True, verbose_name='Creation date')),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datasets', to='main.Schema')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dataset', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('range_from', models.IntegerField(blank=True, null=True, verbose_name='Range from')),
                ('range_to', models.IntegerField(blank=True, null=True, verbose_name='Range to')),
                ('column_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='columns', to='main.Column_Type')),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='columns', to='main.Schema')),
            ],
        ),
    ]
