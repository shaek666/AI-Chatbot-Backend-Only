from django.urls import path
from .views import (
    ChatSessionListCreateView,
    ChatSessionDetailView,
    MessageListView,
    ChatHistoryView,
    DocumentListCreateView
)

urlpatterns = [
    path('sessions/', ChatSessionListCreateView.as_view(), name='chat-sessions'),
    path('sessions/<int:pk>/', ChatSessionDetailView.as_view(), name='chat-session-detail'),
    path('sessions/<int:session_id>/messages/', MessageListView.as_view(), name='session-messages'),
    path('history/', ChatHistoryView.as_view(), name='chat-history'),
    path('documents/', DocumentListCreateView.as_view(), name='documents'),
]