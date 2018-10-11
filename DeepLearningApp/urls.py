from django.conf.urls import url, include
from DeepLearningApp import views
from DeepLearningApp.model import regression
from django.urls import path

urlpatterns = [
    path('add_book', views.add_book),
    path('show_books', views.show_books),
    path('upload_file', views.upload_file),
    path('analyseSample', views.analyseSample),
    path('startTraining', regression.startTraing)
    # url(r'add_book$', views.add_book,),
    # url(r'show_books$', views.show_books)
]
