from django.contrib import admin
from .models import Chat, UserProfile, UserProfileImage, Message
# Register your models here.


class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'created')
    filter_horizontal = ('participants',)  # Alternatively, you can use filter_vertical


admin.site.register(Chat, ChatAdmin)
admin.site.register(UserProfile)
admin.site.register(UserProfileImage)
admin.site.register(Message)
