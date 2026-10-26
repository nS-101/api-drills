import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Note

# Tip: write a small helper that turns a Note into a dict first;
# every endpoint needs it.
