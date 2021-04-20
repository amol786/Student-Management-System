from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .models import StudentInfo
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages
from .forms import CreateStudent
from django.contrib.auth.decorators import permission_required

import csv, io,logging

# Create your views here.
def students_list(request):
    students = StudentInfo.objects.all()
    #students = StudentInfo.objects.all().order_by('first_name','admission_date')
    #if request.GET.get('sort_by'):
    #    students = StudentInfo.objects.all().order_by('first_name','admission_date')
    paginator = Paginator(students, 10)
    page = request.GET.get('page')
    paged_students = paginator.get_page(page)
 
    context = {
        "students": paged_students
    }
    return render(request, "students/student_list.html", context)

def sort_list(request):
    sort_column = request.GET.get('sort_by')
    sorted_student = StudentInfo.objects.all().order_by('first_name','admission_date')
    context = {
        "students": sorted_student
    }
    return render(request, "students/student_list.html", context)

@permission_required("auth.view_students")
def student_detail(request,student_id):
    #students = get_object_or_404(StudentInfo, pk = student_id)
    try:
        students = StudentInfo.objects.get(pk=student_id)
    except StudentInfo.DoesNotExist:
        raise Http404("Given Student Id is not found")
    context = {
        "students": students,
    }
    return render(request,"students/student_detail.html",context)

@permission_required("auth.change_students")
def edit_student(request, student_id):
    student_edit = StudentInfo.objects.get(pk=student_id)
    edit_forms = CreateStudent(instance=student_edit)

    if request.method == "POST":
        edit_forms = CreateStudent(request.POST, instance=student_edit)

        if edit_forms.is_valid():
            edit_forms.save()
            messages.success(request, "Edit Student Info succesfully")

            return redirect("students_list")
    
    context = {
        "edit_forms": edit_forms
    }

    return render(request,"students/edit_student.html",context)

@permission_required("auth.delete_students")
def delete_student(request, student_id):
    #if request.user.is_superuser():
    student_delete = StudentInfo.objects.get(id=student_id)
    student_delete.delete()
    messages.success(request, "Delete Student Info Successfully")
    
    return redirect("students_list")

@permission_required("auth.view_students")
def download_csv(request):
    students = StudentInfo.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="csv_database.csv"'
    writer = csv.writer(response)
    writer.writerow(['id','first_name', 'last_name', 'registeration_num', 'admission_date','gender','created_dt','modify_dt'])

    for student in students:
        writer.writerow([ student.id, student.first_name, student.last_name, student.registeration_num, student.admission_date,
        student.gender, student.created_dt,student.modify_dt])

    return response

@permission_required("auth.view_students")
def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "students/student_upload.html", data)
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("students: upload_csv"))

            
        file_data = csv_file.read().decode("utf-8")		
        
        lines = file_data.split("\n")
        
        #loop over the lines and save them in db. If error , store as string and then displa
        for line in lines:
            fields = line.split(",")
            data_dict = {}
            data_dict["first_name"] = fields[0]
            data_dict["last_name"] = fields[1]
            data_dict["registeration_num"] = fields[2]
            data_dict["admission_date"] = fields[3]
            data_dict["gender"] = fields[4].strip()
            print(data_dict)
            try:
                form = CreateStudent(data_dict)
                if form.is_valid():
                    form.save()
                else:
                    logging.getLogger("error_logger").error(form.errors.as_json())												
            except Exception as e:
                logging.getLogger("error_logger").error(repr(e))
                pass
    
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))
        
    return redirect("students_list")
    