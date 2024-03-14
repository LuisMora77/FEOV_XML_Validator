from django.shortcuts import render
from django.http import HttpResponse
from . import main
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def index(request):
    typeEinvoice = request.headers['typeEinvoice']
    docType = request.headers['docType']
    xml = request.body.decode('UTF-8')
    return HttpResponse(main.runPath(xml, typeEinvoice,docType))




