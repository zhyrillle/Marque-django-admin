# organizations/serializers.py
from rest_framework import serializers
from .models import Organization, OrgOfficer, JoinRequest, FollowedOrgs

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class OrgOfficerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgOfficer
        fields = '__all__'

class JoinRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinRequest
        fields = '__all__'

class FollowedOrgsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowedOrgs
        fields = '__all__'