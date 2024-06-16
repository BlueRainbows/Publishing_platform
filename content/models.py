from django.db import models
from users.models import User


class Content(models.Model):
    """ Модель содержимого платформы """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        blank=True,
        null=True
    )
    title = models.CharField(
        max_length=100,
        verbose_name='Заголовок'
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    image = models.ImageField(
        upload_to='content/',
        verbose_name='Изображение'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    publish = models.BooleanField(
        default=False,
        verbose_name='Опубликовано'
    )
    views = models.PositiveIntegerField(
        default=0,
        verbose_name='Просмотры'
    )
    subscribers = models.PositiveIntegerField(
        default=0,
        verbose_name='Подписчики'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Контент'
        verbose_name_plural = 'Контент'
        ordering = ['-created_at']

        permissions = [
            ("change_publish", "Изменение флага публикации"),
        ]


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата создания коментария'
    )
    comment = models.CharField(
        max_length=500,
        verbose_name='Текст коментария'
    )

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'


class LikeCount(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
