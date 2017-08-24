from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.core.cache import cache
from django.utils import timezone
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import os
import django
import base64
from PIL import Image
from io import BytesIO
import json


from . import ocr
from . import get_words

os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
django.setup()

ROOT = os.path.dirname(os.path.abspath(__file__))


def main(request):
    recognised_letters = ""
    if request.method == 'GET':
        print("GET request")
    else:
        print("POST request")
        print(request)
        json_str = ((request.body).decode('utf-8'))
        json_obj = json.loads(json_str)
        photo = json_obj['photo']
        print(photo)
        print(type(photo))

        im = Image.open(BytesIO(base64.b64decode(photo)))
        im.save("word_finder/test.png", 'PNG')


        recognised_letters = ocr.detect_letters("word_finder/s1.png")


    return JsonResponse({"result": recognised_letters})

def compute(request):
    words = []
    new_dict = {}
    if request.method == 'GET':
        print("GET request")
    else:
        print("POST request")
        print(request)
        json_str = ((request.body).decode('utf-8'))
        json_obj = json.loads(json_str)
        letters = json_obj['input']
        print(letters)

        print("Start computing")
        words = get_words.get_words(letters)
        words = [(item[0], ' '.join([str(pair[0]) + ' ' + str(pair[1]) for pair in item[1]])) for item in words]

        print(words)
        for item in words:
            new_dict[item[0]] = item[1]
    return JsonResponse({"result": new_dict})
