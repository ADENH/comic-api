from django.shortcuts import render
from rest_framework import viewsets
import requests
from bs4 import BeautifulSoup
from django.views.decorators.csrf import csrf_exempt

from .serializers import ComicSerializer
from .models import ComicPopular
import json
from django.http import JsonResponse
import re
import urllib
from rest_framework.decorators import api_view


# Create your views here.
BASE_URL = "https://kiryuu.id/"

class ComicViewSet(viewsets.ModelViewSet):
    ComicPopular.objects.all().delete()
    page = requests.get(BASE_URL, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(page.text, 'html.parser')
    popular = soup.find("div", {"class": "bixbox hothome full"})
    popular = popular.findAll("div", {"class": "bsx"})
    popular_url = []
    for data in popular:
        link = data.find('a')
        comic_url = link['href']
        thumbnail = data.find("img", {"class": "ts-post-image"})
        thumbnail_url = thumbnail['src']
        title = data.find("div", {"class": "tt"}).text.strip()
        chapter = data.find("div", {"class": "epxs"}).text
        rating = data.find("div", {"class": "numscore"}).text
        type_comic = data.find("span", {"class": "type"})
        type_comic = type_comic['class'][1]
        comic_data = [comic_url, thumbnail_url, title, type_comic, chapter, rating]
        popular_url.append(comic_data)
        ComicPopular.objects.create(
            title=title,
            description="",
            status="",
            release="",
            artist="",
            type=type_comic,
            thumbnail=thumbnail_url,
            chapter=chapter,
            comic_url=comic_url,
            rating=rating
        )

    queryset = ComicPopular.objects.all().order_by('title')
    serializer_class = ComicSerializer


@csrf_exempt
def detail_comic(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = body['comic_url']
    comic_url = request.POST.get('comic_url')
    page = requests.get(content, headers={'User-Agent': 'Mozilla/5.0'})
    # print(page.text)
    soup = BeautifulSoup(page.text, 'html.parser')
    title = soup.find("h1", {"class": "entry-title"}).text
    datas = soup.find("div", {"class": "postbody"})
    description = datas.find("div", {"class": "entry-content"}).text.strip()
    rating = datas.find("div", {"class": "rating"}).text.strip()
    chapterlist = datas.findAll("div", {"class": "eph-num"})
    allChapter = []
    for chapter in chapterlist:
        chapter = chapter.find("a")
        chapter_url = chapter['href']
        chapter_num = chapter.find("span", {"class": "chapternum"}).text
        chapter_date = chapter.find("span", {"class": "chapterdate"}).text
        if "{{number}}" in chapter:
            continue;
        if "{{number}}" in chapter_num:
            continue;
        if "{{date}}" in chapter_date:
            continue;
        data = {
            "chapter_url": chapter_url,
            "chapter_num": chapter_num,
            "chapter_date": chapter_date
        }
        allChapter.append(data)

    comic_detail = {
        "title": title,
        "description": description,
        "rating": rating,
        "chapter_list": allChapter
    }
    body_response = {
        "data": comic_detail
    }
    return JsonResponse(body_response)

@csrf_exempt
def popular_comic(request):
    page = requests.get(BASE_URL, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(page.text, 'html.parser')
    popular = soup.find("div", {"class": "bixbox hothome full"})
    popular = popular.findAll("div", {"class": "bsx"})
    popular_url = []
    for data in popular:
        link = data.find('a')
        comic_url = link['href']
        thumbnail = data.find("img", {"class": "ts-post-image"})
        thumbnail_url = thumbnail['src']

        if not thumbnail_url.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif','webp')):
            thumbnail_url = thumbnail['data-lazy-src']

        title = data.find("div", {"class": "tt"}).text.strip()
        chapter = data.find("div", {"class": "epxs"}).text
        rating = data.find("div", {"class": "numscore"}).text
        type_comic = data.find("span", {"class": "type"})
        type_comic = type_comic['class'][1]
        # comic_data = [comic_url, thumbnail_url, title, type_comic, chapter, rating]
        comic_data = {
            "title": title,
            "type_comic": type_comic,
            "chapter": chapter,
            "rating": rating,
            "comic_url": comic_url,
            "thumbnail_url": thumbnail_url
        }
        popular_url.append(comic_data)
    response = {
        "comics": popular_url
    }
    body_response = {
        "data": response
    }
    return JsonResponse(body_response)

@csrf_exempt
def read_comic(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = body['comic_url']
    page = requests.get(content, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(page.content, 'html.parser')
    soup = soup.find("div", {"id": "content"})
    soup = soup.find("div", {"class": "wrapper"})
    scripts = soup.findAll('script')
    next_url = ""
    prev_url = ""
    for script in scripts:
        if "BELUM ADA CHAPTER" in script.text:
            data = json.loads(script.text[14:-2])
            prev_url = data["prevUrl"]
            next_url = data["nextUrl"]
            break
    datas = soup.find("div", {"id": "readerarea"})
    datas = datas.findAll("img")
    images = []
    x = 1
    for img in datas:
        image_url = img['src']
        # image_index = img['data-index']
        # image_url = urllib.parse.quote(image_url, safe='')
        image = {
            "image_url": image_url,
            "image_index": x
        }
        images.append(image)
        x = x + 1
    response = {
        "image_urls": images,
        "next_url": next_url,
        "prev_url": prev_url
    }
    body_response = {
        "data": response
    }
    return JsonResponse(body_response)

@csrf_exempt
def list_comic(request):
    page = requests.get(BASE_URL, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(page.text, 'html.parser')
    soup = soup.find("div", {"class": "postbody"})
    list_updates = soup.findAll("div", {"class": "listupd"})
    list_update = list_updates[1]

    list_update = list_update.findAll("div", {"class": "utao"})

    comic_data = []
    for comic in list_update:
        comic_url = comic.find("a")["href"]
        comic_title = comic.find("a")["title"]
        comic_thumbnail = comic.find("img")["src"]
        if not imageFile(comic_thumbnail):
            comic_thumbnail = comic.find("img")["data-lazy-src"]
        data = {
            "title": comic_title,
            "type_comic": "",
            "chapter": "",
            "rating": "",
            "comic_url": comic_url,
            "thumbnail_url": comic_thumbnail
        }
        comic_data.append(data)

    list_update0 = list_updates[0]
    list_update0 = list_update0.findAll("div", {"class": "utao"})
    for comic in list_update0:
        comic_url = comic.find("a")["href"]
        comic_title = comic.find("a")["title"]
        comic_thumbnail = comic.find("img")["src"]
        if not imageFile(comic_thumbnail):
            comic_thumbnail = comic.find("img")["data-lazy-src"]
        data = {
            "title": comic_title,
            "type_comic": "",
            "chapter": "",
            "rating": "",
            "comic_url": comic_url,
            "thumbnail_url": comic_thumbnail
        }
        comic_data.append(data)
    response = {
        "data": comic_data
    }
    return JsonResponse(response)

@csrf_exempt
def search_comic(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = body['keyword']
    url = "https://kiryuu.id/?s=" + content
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(page.content, 'html.parser')
    list_updates = soup.find("div", {"class": "bixbox"})
    comics = list_updates.findAll("div", {"class": "bsx"})
    list_comics = []
    for data in comics:
        link = data.find('a')
        comic_url = link['href']
        thumbnail = data.find("img", {"class": "ts-post-image"})
        thumbnail_url = thumbnail['src']
        if not thumbnail_url.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', 'webp')):
            thumbnail_url = thumbnail['data-lazy-src']
        title = data.find("div", {"class": "tt"}).text.strip()
        chapter = data.find("div", {"class": "epxs"}).text
        rating = data.find("div", {"class": "numscore"}).text
        type_comic = data.find("span", {"class": "type"})
        if type_comic is not None:
            type_comic = type_comic['class'][1]
        # comic_data = [comic_url, thumbnail_url, title, type_comic, chapter, rating]
        comic_data = {
            "title": title,
            "type_comic": type_comic,
            "chapter": chapter,
            "rating": rating,
            "comic_url": comic_url,
            "thumbnail_url": thumbnail_url
        }
        list_comics.append(comic_data)
    response = {
        "comics": list_comics
    }
    body_response = {
        "data": response
    }
    return JsonResponse(body_response)


def imageFile(str):
    # Regex to check valid image file extension.
    regex = "([^\\s]+(\\.(?i)(jpe?g|png|gif|bmp|webp|jpg))$)"

    # Compile the ReGex
    p = re.compile(regex)

    # If the string is empty
    # return false
    if (str == None):
        return False

    # Return if the string
    # matched the ReGex
    if (re.search(p, str)):
        return True
    else:
        return False