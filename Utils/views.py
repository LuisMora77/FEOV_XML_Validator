from django.shortcuts import render
import json
import dicttoxml 
from rest_framework import status
from rest_framework.views import APIView
from django.http import HttpResponse

class ConvertJsonToXML(APIView):
    def post(self,request):
        try:
            process  = 'Cargar Datos recibidos'
            list_data = json.loads(request.body)

            process = 'Convercion de json a xml'
            xml = dicttoxml.dicttoxml(list_data)

            return HttpResponse(xml,status=status.HTTP_200_OK)

        except:
            return  HttpResponse('error '+ process ,status=status.HTTP_400_BAD_REQUEST)




