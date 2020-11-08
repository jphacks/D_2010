from django.urls import path
from . import views

app_name = 'lives'

urlpatterns = [
    path('search/', views.SearchYtId, name='SearchYtId'),
    path('addvideo/', views.addVideos, name='addVideos'),
    path('setReaction/',views.setReaction, name='setReaction'),
    path('getReaction/', views.getReaction, name='getReaction'),
    path('searchvideo/', views.SearchVideos, name='SearchVideos'),
]
