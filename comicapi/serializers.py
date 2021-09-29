from rest_framework import serializers

from .models import ComicPopular

class ComicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ComicPopular
        fields = '__all__'