from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SearchHistory(models.Model):
    user = models.ForeignKey(User, related_name='history', on_delete=models.CASCADE)
    city = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField()


    def __str__(self):
        return self.user


