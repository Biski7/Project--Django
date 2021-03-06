# Generated by Django 3.1.1 on 2020-09-15 14:11

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20200915_1746'),
    ]

    operations = [
        migrations.CreateModel(
            name='MajorItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=500)),
                ('Imdb_rating', models.FloatField(blank=True)),
                ('Image', models.ImageField(upload_to='media')),
                ('Genre', multiselectfield.db.fields.MultiSelectField(choices=[('ACT', 'ACTION'), ('ADV', 'ADVENTURE'), ('COM', 'COMEDY'), ('CR', 'CRIME'), ('SCI-FY', 'SCI-FY'), ('ANI', 'ANIMATION'), ('HOR', 'HORROR'), ('SH', 'SUPERHERO'), ('DR', 'DRAMA')], default='basic', max_length=35)),
            ],
        ),
        migrations.CreateModel(
            name='Trailers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=500)),
                ('Image', models.ImageField(upload_to='media')),
                ('Video', models.TextField(max_length=500)),
                ('Length', models.TextField(max_length=200)),
            ],
        ),
    ]
