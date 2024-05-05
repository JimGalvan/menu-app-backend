import uuid

from django.db import models


class BaseModel(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Restaurant(BaseModel):
    owner = models.ForeignKey('auth.User', default=uuid.uuid4(), related_name='restaurants', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    website = models.URLField(max_length=100, null=True)
    description = models.TextField(null=True)
    logo = models.ImageField(upload_to='images/', null=True)

    def __str__(self):
        return self.name


class Menu(BaseModel):
    restaurant = models.ForeignKey(Restaurant, default=uuid.uuid4(), related_name='menus', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name
