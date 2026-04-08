from rest_framework import serializers
from .models import Organization, OrgOfficer, JoinRequest, FollowedOrgs
from departments.models import Department

class OrganizationSerializer(serializers.ModelSerializer):
    _id = serializers.CharField(read_only=True, required=False)
    
    department_id = serializers.ChoiceField(choices=[])

    class Meta:
        model = Organization
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self.fields['department_id'].choices = [
                (str(dept._id), f"{dept.department_code} - {dept.department_name}") 
                for dept in Department.objects.all()
            ]
        except:
            self.fields['department_id'].choices = []

    def to_representation(self, instance):
        """ This is the 'Filter' that prevents the JSON Serializer error """
        ret = super().to_representation(instance)
        
        if '_id' in ret and not isinstance(ret['_id'], str):
            ret['_id'] = str(ret['_id'])
            
        if 'department_id' in ret and not isinstance(ret['department_id'], str):
            ret['department_id'] = str(ret['department_id'])
            
        return ret

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