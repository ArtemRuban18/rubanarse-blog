from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from slugify import slugify


class Category(models.Model):
    """
    Model for category of posts

    Fields:
        - title: CharField
        - slug: SlugField
    """

    title = models.CharField(max_length=255,blank=False)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Post(models.Model):
    """
    Model for posts

    STATUS_POST: tuple

    Defines possible statuses for a post.

    Available statuses:
    - 'checkout'`: 'На перевірці' (Pending review)
    - 'published'`: 'Опубліковано' (Published)

    Fields:
        - title: CharField
        - category: ForeignKey
        - content: RichTextUploadingField
        - slug: SlugField
        - author: ForeignKey
        - created_at: DateTimeField
        - updated_at: DateTimeField
        - views: PosititveIntegerField
        - status: CharField
    """

    STATUS_POST = (
        ('checkout','На перевірці'),
        ('published','Опубліковано')
    )

    title = models.CharField(blank = False, unique=True, max_length=255)
    category = models.ForeignKey(Category, blank = False, on_delete=models.CASCADE, default=0)
    content = RichTextUploadingField(blank = False)
    slug = models.SlugField(blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    status = models.CharField(blank=False, choices=STATUS_POST, default='checkout')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    """
    Model for post comments

    Fields:
        - user: ForeignKey
        - post: ForeignKey
        - comment: CharField
        - created_at: DateTimeField
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} commited {self.post.title}"
