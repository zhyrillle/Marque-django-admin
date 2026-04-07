from django.urls import path
from .views import EventListCreateView, EventRetrieveUpdateDeleteView

urlpatterns = [
    path('', EventListCreateView.as_view(), name='event-list-create'),
    path('<str:pk>/', EventRetrieveUpdateDeleteView.as_view(), name='event-detail'),
]