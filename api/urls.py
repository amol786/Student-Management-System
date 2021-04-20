from django.urls import path
from django.conf.urls import url
from .views import StudentCreate,StudentDetail

urlpatterns = [
    path('<str:pk>/', StudentDetail.as_view()),
    path('', StudentCreate.as_view()),
]