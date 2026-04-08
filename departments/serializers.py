from rest_framework import serializers
from .models import Department
from colleges.serializers import CollegeSerializer
from colleges.models import College

class DepartmentSerializer(serializers.ModelSerializer):
    _id = serializers.CharField(read_only=True, required=False)
    college = CollegeSerializer(read_only=True)
    college_id = serializers.PrimaryKeyRelatedField(
        queryset=College.objects.all(), source='college', write_only=True
    )

    class Meta:
        model = Department
        fields = ['_id', 'department_code', 'department_name', 'college', 'college_id']

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        if '_id' in ret and not isinstance(ret['_id'], str):
            ret['_id'] = str(ret['_id'])

        if 'college_id' in ret and not isinstance(ret['college_id'], str):
            ret['college_id'] = str(ret['college_id'])
        return ret