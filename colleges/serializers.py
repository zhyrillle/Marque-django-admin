from rest_framework import serializers
from .models import College

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['id', 'college_code', 'college_name']