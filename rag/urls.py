from django.urls import path
from .views import ChatBotView, DocumentIndexView

urlpatterns = [
    path('chat/', ChatBotView.as_view(), name='chatbot'),
    path('index-documents/', DocumentIndexView.as_view(), name='index-documents'),
]