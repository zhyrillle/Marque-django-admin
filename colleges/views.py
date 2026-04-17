from rest_framework import viewsets
from .models import College
from .serializers import CollegeSerializer
from users.permissions import IsAdminOrReadOnly

class CollegeViewSet(viewsets.ModelViewSet):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    permission_classes = [IsAdminOrReadOnly]