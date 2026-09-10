from django.db import models
from django.contrib.auth.models import User

class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    high_score = models.IntegerField(default=0)
    current_level = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username