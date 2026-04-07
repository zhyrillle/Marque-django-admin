from bson import ObjectId
from rest_framework import serializers


def to_object_id(value):
    """Convert a string to a bson ObjectId, raise ValidationError if invalid."""
    if not ObjectId.is_valid(value):
        raise serializers.ValidationError(f"'{value}' is not a valid ObjectId.")
    return ObjectId(value)


def filter_by_object_id(queryset, field, str_id):
    """Safely filter a queryset by a MongoDB ObjectId string."""
    if not ObjectId.is_valid(str_id):
        return queryset.none()
    return queryset.filter(**{field: ObjectId(str_id)})