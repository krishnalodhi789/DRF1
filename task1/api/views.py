from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .serializer import StudentSerializer
from .models import Student
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser,ParseError
from django.views.decorators.csrf import csrf_exempt
import json
import io

# Create your views here.
def student_info(request,id):
    stu = Student.objects.get(pk=id)
    serialize = StudentSerializer(stu)
    return JsonResponse(serialize.data)
    
    # data= JSONRenderer().render(serialize.data)
    # print(data)
    # return HttpResponse(data, content_type = 'application/json')
    
    
def student_list(request):
    stu_list = Student.objects.all()
    serializer = StudentSerializer(stu_list, many=True)
    # return JsonResponse(serializer.data,safe=False)

    data= JSONRenderer().render(serializer.data)
    print(data)
    return HttpResponse(data, content_type = 'application/json')
    
@csrf_exempt          
def stu_regi(req):
    if req.method == "POST":
        parsed_data = JSONParser().parse(req)
        serializer = StudentSerializer(data=parsed_data)
        if serializer.is_valid():
            serializer.save()
            res = {'message': "Created.."}
            data= JSONRenderer().render(serializer.data)
            return HttpResponse(data, content_type='application/json')
            
        error= JSONRenderer().render(serializer.errors)
        print(" Errpr==============")
        print(error)
        return HttpResponse(error, content_type='application/json',)
            
            
@csrf_exempt
def insert_stu_list(request):
    if request.method == 'POST':
        parse_data = JSONParser().parse(request)
        serializer = StudentSerializer(data=parse_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        
        data = JSONParser().parse(serializer.errors)
        return JsonResponse(data, safe=False)
        
        