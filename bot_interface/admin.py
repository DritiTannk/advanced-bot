from django.contrib import admin
from .models import User, UserChatHistory


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name',
                    'created_at',
                    )


class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'user_msg',
                    'bot_resp', 'created_at',
                    )


admin.site.register(User, UserAdmin)
admin.site.register(UserChatHistory, ChatHistoryAdmin)

