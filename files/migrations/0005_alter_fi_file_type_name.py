# Generated by Django 4.0.3 on 2022-04-21 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0004_alter_fi_file_type_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fi_file_type',
            name='name',
            field=models.TextField(),
        ),
    ]