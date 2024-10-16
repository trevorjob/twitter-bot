from django.contrib import admin
from .models import Tweets


# Register your models here.
class TweetAdmin(admin.ModelAdmin):
    list_display = ["message", "created_at", "post_time", "status", "id"]


admin.site.register(Tweets, TweetAdmin)
