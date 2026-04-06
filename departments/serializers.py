from rest_framework import serializers
from .models import Department
from colleges.serializers import CollegeSerializer
from colleges.models import College

class DepartmentSerializer(serializers.ModelSerializer):
    college = CollegeSerializer(read_only=True)
    college_id = serializers.PrimaryKeyRelatedField(
        queryset=College.objects.all(), source='college', write_only=True
    )

    class Meta:
        model = Department
        fields = ['id', 'department_code', 'department_name', 'college', 'college_id']