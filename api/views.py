from django.shortcuts import render
from rest_framework import generics, filters, pagination, permissions

from students.models import StudentInfo
from .serializers import StudentInfoSerializer
from rest_framework_swagger.views import get_swagger_view

# Create your views here.

#schema_view = get_swagger_view(title='StudentS Management System API')

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class StudentCreate(generics.ListCreateAPIView):
    queryset = StudentInfo.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id', 'first_name']
    ordering_fields = '__all__'
    pagination_class = StandardResultsSetPagination
    serializer_class = StudentInfoSerializer

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentInfo.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = StudentInfoSerializer