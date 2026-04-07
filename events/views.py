from rest_framework import generics, status
from rest_framework.response import Response
from .models import Event, AttendanceLog, Bookmark, Feedback
from .serializers import (
    EventSerializer,
    AttendanceLogSerializer,
    BookmarkSerializer,
    FeedbackSerializer,
)


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class AttendanceLogListCreateView(generics.ListCreateAPIView):
    queryset = AttendanceLog.objects.all()
    serializer_class = AttendanceLogSerializer


class AttendanceLogRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AttendanceLog.objects.all()
    serializer_class = AttendanceLogSerializer


class BookmarkListCreateView(generics.ListCreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer


class BookmarkRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer


class FeedbackListCreateView(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class FeedbackRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer