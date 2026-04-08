from rest_framework import serializers
from .models import College

class CollegeSerializer(serializers.ModelSerializer):
    _id = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = College
        fields = ['_id', 'college_code', 'college_name']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if '_id' in ret and not isinstance(ret['_id'], str):
            ret['_id'] = str(ret['_id'])
        return ret