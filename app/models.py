from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Blog(models.Model):
    text = models.TextField(max_length=2000)
    title = models.CharField(max_length=100)
    #지금 로그인한 유저를 여기 때려 박겠다!
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default = 1, on_delete = models.CASCADE)   #이거랑 time은 웬만하면 넣어주면 좋대
    time = models.DateTimeField(default = timezone.now)  #미국시간기준

