from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Event, AttendanceLog, Bookmark, Feedback
from .serializers import (
    EventSerializer,
    AttendanceLogSerializer,
    BookmarkSerializer,
    FeedbackSerializer,
)
from users.permissions import IsAdminOrReadOnly
from bson import ObjectId


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = '_id'
    lookup_url_kwarg = 'pk'

    # Override to convert string to ObjectId
    def get_object(self):
        _id = self.kwargs.get(self.lookup_url_kwarg)
        try:
            return Event.objects.get(_id=ObjectId(_id))
        except Event.DoesNotExist:
            raise NotFound("Event not found.")

class AttendanceLogListCreateView(generics.ListCreateAPIView):
    queryset = AttendanceLog.objects.all()
    serializer_class = AttendanceLogSerializer
    permission_classes = [IsAuthenticated]


class AttendanceLogRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AttendanceLog.objects.all()
    serializer_class = AttendanceLogSerializer
    permission_classes = [IsAdminOrReadOnly]


class BookmarkListCreateView(generics.ListCreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]


class BookmarkRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]


class FeedbackListCreateView(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]


class FeedbackRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
