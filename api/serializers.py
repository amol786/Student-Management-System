from rest_framework import serializers
from students.models import StudentInfo

class StudentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentInfo
        fields ='__all__'