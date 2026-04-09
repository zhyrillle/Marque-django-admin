from rest_framework import serializers
from .models import Event, AttendanceLog, Bookmark, Feedback
from organizations.models import Organization
from bson import ObjectId
from .utils import filter_by_object_id


class ObjectIdField(serializers.Field):
    """Handles serialization/deserialization of MongoDB ObjectId fields."""

    def to_representation(self, value):
        # ObjectId → string for GET responses
        return str(value)

    def to_internal_value(self, data):
        # string → validate on POST/PUT
        if not ObjectId.is_valid(str(data)):
            raise serializers.ValidationError("Invalid ObjectId format.")
        return str(data)  # keep as string; model CharField stores it as string


class EventSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(required=False)
    event_image_file = serializers.ImageField(write_only=True, required=False)
    organization_id = serializers.ChoiceField(choices=[])
    remindersSent = serializers.JSONField(required=False)  # ✅ keep as JSONField

    class Meta:
        model = Event
        fields = [
            '_id',
            'organization_id',
            'event_name',
            'event_type',
            'description',
            'event_image',
            'event_image_file',
            'event_date',
            'end_date',
            'start_time',
            'end_time',
            'venue',
            'venue_details',
            'status',
            'is_mandatory',
            'remindersSent',
            'reminders_twentyFourHours',
            'reminders_oneHour',
            'reminders_conclusion',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        choices = []

        for org in Organization.objects.all():
            try:
                org_id = str(org._id)
                org_name = getattr(org, 'org_name', None) or "Unnamed Org"
                choices.append((org_id, org_name))
            except Exception as e:
                print("ORG ERROR:", e)

        self.fields['organization_id'].choices = choices

    def validate_organization_id(self, value):
        if not ObjectId.is_valid(value):
            raise serializers.ValidationError("Invalid MongoDB ObjectId.")

        if not filter_by_object_id(Organization.objects, '_id', value).exists():
            raise serializers.ValidationError("Organization not found.")

        return value

    # =========================
    # ✅ CREATE
    # =========================
    def create(self, validated_data):
        image_file = validated_data.pop('event_image_file', None)

        # ✅ Extract virtual fields
        reminders = validated_data.get('remindersSent', {}) or {}

        reminders["twentyFourHours"] = validated_data.pop(
            'reminders_twentyFourHours',
            reminders.get("twentyFourHours", False)
        )
        reminders["oneHour"] = validated_data.pop(
            'reminders_oneHour',
            reminders.get("oneHour", False)
        )
        reminders["conclusion"] = validated_data.pop(
            'reminders_conclusion',
            reminders.get("conclusion", False)
        )

        validated_data['remindersSent'] = reminders

        if image_file:
            import cloudinary.uploader
            result = cloudinary.uploader.upload(image_file)
            validated_data['event_image'] = result['secure_url']

        return super().create(validated_data)

    # =========================
    # ✅ UPDATE (fix duplicate creation)
    # =========================
    def update(self, instance, validated_data):
        # ✅ Always preserve the original _id
        validated_data['_id'] = instance._id
    
        image_file = validated_data.pop('event_image_file', None)
        reminders = instance.remindersSent or {}
    
        if 'reminders_twentyFourHours' in validated_data:
            reminders["twentyFourHours"] = validated_data.pop('reminders_twentyFourHours')
    
        if 'reminders_oneHour' in validated_data:
            reminders["oneHour"] = validated_data.pop('reminders_oneHour')
    
        if 'reminders_conclusion' in validated_data:
            reminders["conclusion"] = validated_data.pop('reminders_conclusion')
    
        validated_data['remindersSent'] = reminders
    
        if image_file:
            import cloudinary.uploader
            result = cloudinary.uploader.upload(image_file)
            validated_data['event_image'] = result['secure_url']
    
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['_id'] = str(instance._id)
        ret['organization_id'] = str(instance.organization_id)
        return ret


class AttendanceLogSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(required=False)

    class Meta:
        model = AttendanceLog
        fields = '__all__'


class BookmarkSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(required=False)

    class Meta:
        model = Bookmark
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(required=False)

    class Meta:
        model = Feedback
        fields = '__all__'