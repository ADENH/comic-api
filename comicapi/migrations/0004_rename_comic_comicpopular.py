# Generated by Django 3.2.7 on 2021-09-28 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comicapi', '0003_comic_rating'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comic',
            new_name='ComicPopular',
        ),
    ]
