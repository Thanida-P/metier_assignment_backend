from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid
import os

def blog_cover_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f"blogs/covers/{uuid.uuid4().hex}{ext}"

def blog_extra_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f"blogs/extra/{uuid.uuid4().hex}{ext}"

thai_number_validator = RegexValidator(
    regex=r'^[ก-๙0-9\s]+$',
    message="Comment must contain only Thai characters and numbers."
)

class BlogStatus(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        
class CommentStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True)
    summary = models.CharField(max_length=500, blank=True)
    content = models.TextField()
    cover_image = models.ImageField(upload_to=blog_cover_upload_path)
    view_count = models.IntegerField(default=0)
    posted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=BlogStatus.choices,
        default=BlogStatus.DRAFT
    )

class BlogExtraImg(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="extra_images")
    image = models.ImageField(upload_to=blog_extra_upload_path)
    order = models.PositiveSmallIntegerField(default=0)

class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name="comments", on_delete=models.CASCADE)
    author_name = models.CharField(max_length=100)
    content = models.TextField(validators=[thai_number_validator])
    posted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=CommentStatus.choices,
        default=CommentStatus.PENDING
    )
    
class UserManager(BaseUserManager):
    def create_user(self, username, password):
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username