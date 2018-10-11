# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from DeepLearningApp.models import Book
from django.http import JsonResponse
import json
# from rest_framework import serializers
from django.core import serializers
import pymysql
# Create your views here.
@require_http_methods(["GET"])
def add_book(request):
    response = {}
    try:
        book = Book(book_name=request.GET.get('book_name'))
        book.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@require_http_methods(["GET"])
def show_books(request):
    response = {}
    try:
        books = Book.objects.filter()
        response['list'] = json.loads(serializers.serialize("json", books))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@csrf_exempt
@require_http_methods(["POST"])
def upload_file(request):
    print("upload file")
    file = request.FILES
    print(file)
    print(file.get('name'))

@require_http_methods(["GET"])
def analyseSample(request):
    dataset = request.GET.get("dataset")
    response = {}
    if(dataset == "regression"):
        cnx = pymysql.connect(user='root', password='butyuhao',
                              host='127.0.0.1',
                              database='DeepLearningArchitecture')
        cursor = cnx.cursor()
        sql = "select * from regression"
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        columns = ['id', 'x', 'y']
        colums2 = ['x', 'y']

        rows = []
        point = []
        counts = 0
        training = 0
        testing = 0
        i = 0
        for row in results:
            i = i + 1
            tmp = {}
            tmp2 = {}
            tmp['id'] = str(row[0])
            tmp['x'] = float(row[1])
            tmp['y'] = float(row[2])
            tmp2['x'] = float(row[1])
            tmp2['y'] = float(row[2])
            rows.append(tmp)
            point.append(tmp2)
        counts = i
        training = counts * 0.8
        testing = counts * 0.2
        result = {}
        result['columns'] = columns
        result['rows'] = rows


        result2 = {}
        result2['columns'] = colums2
        tmpPoint = {}
        tmpPoint['Point'] = point
        result2['rows'] = tmpPoint

        static = {}
        static['counts'] = counts
        static['training'] = training
        static['testing'] = testing

        response['result'] = result
        response['result2'] = result2
        response['static'] = static
        response['msg'] = 'success'
        response['error_num'] = 0
        cursor.close()
        cnx.close()
        return JsonResponse(response)
    if(dataset == "pollutant"):
        cnx = pymysql.connect(user='root', password='butyuhao',
                              host='127.0.0.1',
                              database='DeepLearningArchitecture')
        cursor = cnx.cursor()
        sql = "select id, PM25, PM10, Co, No2, So2, O3 from city"
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        rows = []
        rowsscatter = []
        i = 0
        for row in results:
            i = i + 1
            tmp = {}
            tmp2 = {}
            if (i <= 1000):
                tmp['id'] = str(row[0])
                tmp['PM2.5'] = float(row[1])
                tmp['PM10'] = float(row[2])
                tmp['CO'] = float(row[3])
                tmp['NO_2'] = float(row[4])
                tmp['SO_2'] = float(row[5])
                tmp['O_3'] = float(row[6])
                rows.append(tmp)
            if(i <= 100):
                tmp2['id'] = str(row[0])
                tmp2['PM2.5'] = float(row[1])
                tmp2['PM10'] = float(row[2])
                rowsscatter.append(tmp2)

        counts = i
        training = int(counts * 0.8)
        testing = int(counts * 0.2)
        cursor.close()
        cnx.close()

        columns = ['id', 'PM2.5', 'PM10', 'CO', 'NO_2', 'SO_2', 'O_3']
        colums2 = ['id', 'PM2.5', 'PM10']

        result = {}
        result['columns'] = columns
        result['rows'] = rows

        resultscatter = {}
        resultscatter['columns'] = colums2
        resultscatter['rows'] = rowsscatter

        static = {}
        static['counts'] = counts
        static['training'] = training
        static['testing'] = testing

        response['result'] = result
        response['result2'] = resultscatter
        response['static'] = static
        response['msg'] = 'success'
        response['error_num'] = 0
        return JsonResponse(response)
