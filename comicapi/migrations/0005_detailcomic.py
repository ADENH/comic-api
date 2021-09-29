# Generated by Django 3.2.7 on 2021-09-28 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comicapi', '0004_rename_comic_comicpopular'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailComic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=225)),
                ('description', models.TextField()),
                ('status', models.CharField(max_length=100)),
                ('release', models.CharField(max_length=100)),
                ('artist', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=100)),
                ('thumbnail', models.CharField(max_length=300)),
                ('update_on', models.CharField(max_length=300)),
                ('chapter', models.CharField(max_length=255)),
                ('comic_url', models.CharField(max_length=500)),
                ('rating', models.CharField(max_length=500)),
            ],
        ),
    ]
