# Generated by Django 4.0.3 on 2022-04-30 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fi_file',
            name='fileType',
            field=models.ForeignKey(help_text='Seleccione...', on_delete=django.db.models.deletion.CASCADE, to='files.fi_file_type', verbose_name='Grupo:'),
        ),
    ]
