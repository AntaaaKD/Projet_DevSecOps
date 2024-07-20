from django.urls import path
from . import views

app_name = 'Wakhtane'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/chat/', views.chat_section, name='chat_section'),
    path('dashboard/group/', views.group_section, name='group_section'),
    path('dashboard/video/', views.video_section, name='video_section'),

    path('chats/new/', views.chat_create_view, name='chat_create'),
    path('chats/<int:chat_id>/', views.chat_detail_view, name='chat_detail'),
    path('chats/<int:chat_id>/message/', views.create_message, name='create_message'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('contacts/', views.contact_list_view, name='contact_list'),
    path('group-discussions/', views.group_discussion_list_view, name='group_discussion_list'),
    path('group/discussion/<int:pk>/', views.group_discussion_detail_view, name='group_discussion_detail'),
    path('group/discussion/<int:pk>/create_message/', views.create_group_message_view, name='create_group_message'),
    path('group/discussion/<int:pk>/delete/', views.group_discussion_delete_view, name='group_discussion_delete'),
    path('group/discussion/<int:pk>/delete_message/', views.delete_group_message, name='delete_group_message'),
    path('group-discussions/new/', views.group_discussion_create_view, name='group_discussion_create'),
    path('chats/<int:chat_id>/delete/', views.chat_delete, name='chat_delete'),
    path('video-calls/', views.video_call_list, name='video_call_list'),
    path('video-calls/new/', views.video_call_create_view, name='video_call_create'),
    path('video-calls/<int:pk>/', views.video_call_detail_view, name='video_call_detail'),
    path('video_call/<int:video_call_id>/delete/', views.delete_video_call, name='video_call_delete'),
]

