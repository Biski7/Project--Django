# Generated by Django 3.1.1 on 2020-09-15 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='totalcart',
            name='cartname',
            field=models.CharField(default='admin', max_length=20),
        ),
    ]
