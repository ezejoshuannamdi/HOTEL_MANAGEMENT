from django.db import models

# Create your models here.

class login_user(models.Model):
    email=models.EmailField(primary_key=True)
    name=models.CharField(max_length=255)
    mobile=models.CharField(max_length=10)
    password=models.CharField(max_length=30)

    def __str__(self):
        return self.email
