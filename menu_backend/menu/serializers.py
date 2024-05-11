from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Menu, Category, MenuItem


class UserSerializer(serializers.HyperlinkedModelSerializer):
    menus = serializers.HyperlinkedRelatedField(many=True, view_name='menu-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'menus']


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Menu
        fields = ['url', 'id', 'name', 'description', 'isActive', 'owner']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    menu = serializers.HyperlinkedRelatedField(view_name='menu-detail', queryset=Menu.objects.all())

    class Meta:
        model = Category
        fields = ['url', 'id', 'name', 'description', 'menu']


class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    menu = serializers.HyperlinkedRelatedField(view_name='menu-detail', queryset=Menu.objects.all())
    category = serializers.HyperlinkedRelatedField(view_name='category-detail', queryset=Category.objects.all())

    class Meta:
        model = MenuItem
        fields = ['url', 'id', 'name', 'description', 'price', 'image', 'category', 'menu']

    def validate(self, data):
        menu = data.get('menu')
        category = data.get('category')

        if category.menu != menu:
            raise serializers.ValidationError("The category must belong to the same menu as the menu item.")

        return data
