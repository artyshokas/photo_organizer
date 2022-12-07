from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from . import models, serializers

User = get_user_model()


class AlbumList(generics.ListCreateAPIView):
    queryset = models.Album.objects.all()
    serializer_class = serializers.AlbumSerializer


class AlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Album.objects.all()
    serializer_class = serializers.AlbumSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        album = models.Album.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if album.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_('You can only delete your created albums'))

    def put(self, request, *args, **kwargs):
        album = models.Album.objects.filter(pk=kwargs['pk'])
        if album.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError(_('You can only update your created albums'))
        

class AlbumPhotoCommentList(generics.ListCreateAPIView):
    serializer_class = serializers.AlbumPhotoCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        album = models.Album.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, album=album)

    def get_queryset(self):
        album = models.Album.objects.get(pk=self.kwargs['pk'])
        return models.AlbumPhotoComment.objects.filter(album=album)


class AlbumPhotoCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.AlbumPhotoComment.objects.all()
    serializer_class = serializers.AlbumPhotoCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        photo = models.AlbumPhotoComment.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if photo.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_('You can delete only your uploaded photos'))

    def put(self, request, *args, **kwargs):
        photo = models.AlbumPhotoComment.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if photo.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError(_('You can update only your uploaded photos'))


class HashtagList(generics.ListCreateAPIView):
    serializer_class = serializers.HashtagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        photo = models.AlbumPhotoComment.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, photo=photo)

    def get_queryset(self):
        photo = models.AlbumPhotoComment.objects.get(pk=self.kwargs['pk'])
        return models.Hashtag.objects.filter(photo=photo)


class HashtagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Hashtag.objects.all()
    serializer_class = serializers.HashtagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        hashtag = models.Hashtag.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if hashtag.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_('You can delete only your added hashtags'))

    def put(self, request, *args, **kwargs):
        hashtag = models.Hashtag.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if hashtag.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError(_('You can update only your posted hashtags'))


class AlbumPhotoCommentLikeCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = serializers.AlbumPhotoCommentLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        photo = models.AlbumPhotoComment.objects.get(pk=self.kwargs['pk'])
        return models.AlbumPhotoCommentLike.objects.filter(user=user, photo=photo)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError(_('You have already liked this photo'))
        user = self.request.user
        photo = models.AlbumPhotoComment.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=user, photo=photo)

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError(_('No likes for this photo'))