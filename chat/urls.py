from django.urls import path, include
from chat import views
from . views import chatList
 
urlpatterns = [
	path('chats', views.chatList, name='chats'),
    #path("<str:room_name>/", views.chatPage, name="room"),
 ]