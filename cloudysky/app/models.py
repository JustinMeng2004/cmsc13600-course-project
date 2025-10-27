# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# This function defines where avatar images will be stored.
def user_avatar_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/avatars/user_<id>/<filename>
    return f'avatars/user_{instance.user.id}/{filename}'

# This function defines where post media files will be stored.
def post_media_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/posts/post_<id>/<filename>
    return f'posts/post_{instance.post.id}/{filename}'


class Profile(models.Model):
    """
    Extends Django's built-in User model to add extra fields.
    """

    # Define choices for the user_type field
    class UserType(models.TextChoices):
        SERF = 'SERF', 'Serf'
        ADMIN = 'ADMIN', 'Administrator'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.SERF
    )
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class ModerationReason(models.Model):
    """
    Stores the pre-approved list of reasons for suppressing content.
    """
    reason_text = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.reason_text


class Post(models.Model):
    """
    Represents a single user-created post in the main feed.
    """
    # related_name='posts' lets us do user.posts.all()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # --- Moderation Fields ---
    is_hidden = models.BooleanField(default=False)
    hidden_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, 
        related_name='hidden_posts',
        null=True,
        blank=True
    )
    hidden_reason = models.ForeignKey(
        ModerationReason,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    hidden_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Post {self.id} by {self.author.username}"

    class Meta:
        # Default ordering: newest first.
        ordering = ['-created_at']


class Comment(models.Model):
    """
    Represents a single comment attached to a Post.
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # --- Moderation Fields (same as Post) ---
    is_hidden = models.BooleanField(default=False)
    hidden_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='hidden_comments',
        null=True,
        blank=True
    )
    hidden_reason = models.ForeignKey(
        ModerationReason,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    hidden_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Comment {self.id} by {self.author.username} on Post {self.post.id}"

    class Meta:
        # Default ordering: oldest first (chronological).
        ordering = ['created_at']


class PostMedia(models.Model):
    """
    A model to attach media (like images) to a Post.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')

    # FileField is more general than ImageField
    media_file = models.FileField(upload_to=post_media_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Media for Post {self.post.id}"
