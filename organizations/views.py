from rest_framework import viewsets
from .models import Organization
from .serializers import OrganizationSerializer
from users.permissions import IsAdminOrReadOnly

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAdminOrReadOnly]