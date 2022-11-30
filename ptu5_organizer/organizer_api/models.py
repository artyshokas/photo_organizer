from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Album(models.Model):
    name = models.CharField(_('Album name'), max_length=20)
    description = models.CharField(_('Description'), max_length=1000)

    def __str__(self) -> str:
        return _("Album name {name}")


class AlbumPhotoComment(models.Model):
    comment = models.TextField(_('comment'), max_length=140)
    album = models.ForeignKey(
        Album,
        verbose_name=_('album'),
        on_delete=models.CASCADE,
        related_name='photos'
    )

    user = models.ForeignKey(
        User,
        verbose_name=_('user'),
        on_delete=models.CASCADE,
        related_name='photos'
    )
    photo = models.ImageField(_('photo'), upload_to='user_photos/', blank=True, null=True)
    attached_at = models.DateTimeField(_('attached_at'), auto_now_add=True)

    class Meta:
        ordering = ('-attached_at', )

    def __str__(self) -> str:
        return _("attached by {user} at {attached_at}").format(
            user=self.user,
            attached_at=self.attached_at,
        )


class Hashtag(models.Model):
    photo = models.ForeignKey(
        AlbumPhotoComment,
        verbose_name=_('photo'),
        on_delete=models.CASCADE,
        related_name='hashtags'
    )
    hashtags = models.TextField(_('hashtags'), max_length=1000)
    user = models.ForeignKey(
        User,
        verbose_name=_('user'),
        on_delete=models.CASCADE,
        related_name='hashtags'
    )

    def __str__(self) -> str:
        return _('Hashtags for {photo_id}').format(
            photo_id=self.id,
            user=self.user
        )

class AlbumPhotoCommentLike(models.Model):
    photo = models.ForeignKey(
        AlbumPhotoComment,
        verbose_name=_('photo'),
        on_delete=models.CASCADE,
        related_name='likes'
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('user'),
        on_delete=models.CASCADE,
        related_name='likes'
    )

    def __str__(self) -> str:
        return f"{self.user} likes {self.photo}"
