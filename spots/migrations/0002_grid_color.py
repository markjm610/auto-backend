# Generated by Django 3.1.5 on 2021-01-19 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spots', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='grid',
            name='color',
            field=models.CharField(default='blue', max_length=200),
        ),
    ]
