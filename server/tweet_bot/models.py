from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.


class Tweets(models.Model):
    class TweetStatus(models.TextChoices):
        PENDING = "PE", _("Pending")
        SUCCESSFUL = "SU", _("Successful")
        FAILED = "FA", _("Failed")

    id = models.CharField(max_length=50, primary_key=True, default=str(uuid4()))
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post_time = models.DateTimeField()
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweets")
    status = models.CharField(
        max_length=2, choices=TweetStatus.choices, default=TweetStatus.PENDING
    )

    def get_status(self) -> TweetStatus:
        # Get value from choices enum
        return self.TweetStatus(self.status)
