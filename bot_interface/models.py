# models.py
from django.db import models


class User(models.Model):
    user_name = models.CharField("userName", max_length=20)
    session_id = models.UUIDField("Session_ID", unique=True)
    meta_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Details"
        verbose_name_plural = "Users Details"

    def __str__(self):
        return f"{self.user_name} | {self.session_id}"


class UserChatHistory(models.Model):
    user = models.ForeignKey(User,
                             verbose_name="User",
                             on_delete=models.CASCADE,
                             related_name='user_chat')
    user_msg = models.TextField("User Message", max_length=1000)
    bot_resp = models.TextField("Bot Response", max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Chat History"
        verbose_name_plural = "Chat History"

    def __str__(self):
        return f"{self.user} | {self.user_msg} | {self.bot_resp}"

