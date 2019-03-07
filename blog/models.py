from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Post(models.Model):
    name = models.CharField('Name', max_length=100)
    slug = models.SlugField('Slug', unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors')
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField('Text', blank=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', blank=False, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', blank=False, null=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f'{self.user} likes \'{self.post.name}\''
