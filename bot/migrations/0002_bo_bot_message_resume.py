# Generated by Django 4.0.3 on 2022-05-16 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bo_bot_message',
            name='resume',
            field=models.CharField(default='test', max_length=70, verbose_name='Abreviatura:'),
        ),
    ]