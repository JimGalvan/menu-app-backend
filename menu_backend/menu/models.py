import uuid

from django.db import models


class BaseModel(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Restaurant(BaseModel):
    owner = models.ForeignKey('auth.User', related_name='restaurants', on_delete=models.CASCADE)
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
    restaurant = models.ForeignKey(Restaurant, related_name='menus', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Category(BaseModel):
    menu = models.ForeignKey(Menu, related_name='categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class MenuItem(BaseModel):
    owner = models.ForeignKey('auth.User', related_name='menu_items', on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='menu_items')
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/', null=True)

    def __str__(self):
        return self.description
