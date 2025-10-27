from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Profile, Post, Comment, ModerationReason, PostMedia

# Register your models here so they appear on the admin site.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(ModerationReason)
admin.site.register(PostMedia)
