from django.contrib import admin
from .models import UserProfile,Post

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_admin')
    list_editable = ('role', 'is_admin')

admin.register(Post)