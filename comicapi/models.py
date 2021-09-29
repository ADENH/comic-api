from django.db import models


# Create your models here.
class ComicPopular(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField()
    status = models.CharField(max_length=100)
    release = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    thumbnail = models.CharField(max_length=300)
    chapter = models.CharField(max_length=255)
    comic_url = models.CharField(max_length=500)
    rating = models.CharField(max_length=500)

    def __str__(self):
        return self.title


class DetailComic(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField()
    status = models.CharField(max_length=100)
    release = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    author = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    thumbnail = models.CharField(max_length=300)
    update_on = models.CharField(max_length=300)
    chapter = models.CharField(max_length=255)
    comic_url = models.CharField(max_length=500)
    rating = models.CharField(max_length=500)

    def __str__(self):
        return self.title

