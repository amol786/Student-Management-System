from django.urls import path
from . import views

urlpatterns =[
    path('',views.students_list,name='students_list'),
    path('first_name/',views.sort_list, name='sort_list'),
    path('<str:student_id>/',views.student_detail , name='student_detail'),
    #path('registration/', views.registration, name='registration'),
    path('edit/<str:student_id>', views.edit_student, name='edit_student'),
    path('delete/<str:student_id>', views.delete_student, name='delete_student'),
    path('export/csv-database/', views.download_csv, name='csv_database'),
    path('import/upload_csv/', views.upload_csv, name="upload_csv"), 
]