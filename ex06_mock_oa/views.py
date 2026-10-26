import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Product
