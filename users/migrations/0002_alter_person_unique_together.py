# Generated by Django 4.0.3 on 2022-05-15 23:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='person',
            unique_together={('phone_number',)},
        ),
    ]
