from django.db import models


class BaseModel(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Menu(BaseModel):
    owner = models.ForeignKey('auth.User', related_name='menus', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Category(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    menu = models.ForeignKey(Menu, related_name='categories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class MenuItem(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/', null=True)
    menu = models.ForeignKey(Menu, related_name='menu_items', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='menu_items', on_delete=models.CASCADE)

    def __str__(self):
        return self.name