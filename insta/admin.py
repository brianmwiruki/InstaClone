from django.contrib import admin
from .models import post

# Register your models here.

admin.site.register(post)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Profile)