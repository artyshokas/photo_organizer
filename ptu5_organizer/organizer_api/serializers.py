from django.contrib.auth import get_user_model
from rest_framework import serializers
from . import models

User = get_user_model()

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model= models.Album
        fields = ('id', 'name', 'description', )


class HashtagSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    photo = serializers.ReadOnlyField(source='photo_id')

    class Meta:
        model = models.Hashtag
        fields = ('id', 'photo', 'hashtags', 'user', 'user_id')


class AlbumPhotoCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    hashtags = HashtagSerializer(many=True, read_only=True)

    class Meta:
        model = models.AlbumPhotoComment
        fields = ('id', 'comment', 'photo', 'user', 'user_id', 'attached_at', 'hashtags')


class AlbumPhotoCommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AlbumPhotoCommentLike
        fields = ('id', )