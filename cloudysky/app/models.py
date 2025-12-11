from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
from django.utils import timezone

# --- Path Functions (Keep these) ---
def user_avatar_path(instance, filename):
    return f'avatars/user_{instance.user.id}/{filename}'

def post_media_path(instance, filename):
    return f'posts/post_{instance.post.id}/{filename}'

# --- MERGED PROFILE MODEL ---
# This contains BOTH your Admin logic (UserType) AND your Color logic.
class Profile(models.Model):
    class UserType(models.TextChoices):
        SERF = 'SERF', 'Serf'
        ADMIN = 'ADMIN', 'Administrator'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # HW7: Critical for Admin permissions
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.SERF
    )
    
    # Standard Fields
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True)
    
    # HW6/Your Custom Feature: The Color Field is KEPT here
    color = models.CharField(max_length=7, default="#808080") 

    def __str__(self):
        return f"{self.user.username}'s Profile"

class ModerationReason(models.Model):
    reason_text = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.reason_text

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_suppressed = models.BooleanField(default=False)
    
    # Moderation Fields
    is_hidden = models.BooleanField(default=False)
    hidden_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='hidden_posts', null=True, blank=True)
    hidden_reason = models.ForeignKey(ModerationReason, on_delete=models.SET_NULL, null=True, blank=True)
    hidden_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post {self.id} by {self.author.username}"

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_suppressed = models.BooleanField(default=False)

    # Moderation Fields
    is_hidden = models.BooleanField(default=False)
    hidden_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='hidden_comments', null=True, blank=True)
    hidden_reason = models.ForeignKey(ModerationReason, on_delete=models.SET_NULL, null=True, blank=True)
    hidden_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment {self.id} on Post {self.post.id}"

class PostMedia(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')
    media_file = models.FileField(upload_to=post_media_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Media for Post {self.post.id}"

# --- SIGNALS (The Logic that Creates the Random Color) ---
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # HERE IS YOUR COLOR LOGIC: We still generate a random HEX color!
        random_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        
        Profile.objects.create(
            user=instance,
            color=random_color,        # Saving the color
            user_type=Profile.UserType.SERF # Defaulting to normal user
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()