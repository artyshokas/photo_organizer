from django.urls import path
from . import views

urlpatterns = [
    path('albums/', views.AlbumList.as_view()),
    path('album/<int:pk>/', views.AlbumDetail.as_view()),
    path('album/<int:pk>/photos', views.AlbumPhotoCommentList.as_view()),
    path('photo/<int:pk>/', views.AlbumPhotoCommentDetail.as_view()),
    path('photo/<int:pk>/hashtags', views.HashtagList.as_view()),
    path('photo/<int:pk>/likes', views.AlbumPhotoCommentLikeCreate.as_view()),
    path('hashtag/<int:pk>/', views.HashtagDetail.as_view()),
]