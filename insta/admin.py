from django.contrib import admin
from .models import post, Image, Comment, Profile

# Register your models here.

admin.site.register(post)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Profile)