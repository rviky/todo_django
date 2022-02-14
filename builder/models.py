from django.db import models
from django.contrib.auth.models import User


class todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    note = models.CharField(max_length=200,verbose_name="to do")
    status = models.BooleanField(default=False)
    created   = models.DateTimeField(auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True, null=True)


    def __str__(self):
        return self.note
