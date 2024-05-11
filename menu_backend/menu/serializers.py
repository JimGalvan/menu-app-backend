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
        fields = ['url', 'id', 'title', 'description', 'isActive', 'owner']

    def validate_title(self, value):
        owner = self.context['request'].user
        queryset = Menu.objects.filter(title=value, owner=owner)

        # Exclude the current instance from the queryset
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("A menu with this title already exists.")
        return value


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    menu = serializers.HyperlinkedRelatedField(view_name='menu-detail', queryset=Menu.objects.all())

    class Meta:
        model = Category
        fields = ['url', 'id', 'name', 'description', 'menu']

    def validate(self, data):
        menu = data.get('menu')
        name = data.get('name')

        queryset = Category.objects.filter(name=name, menu=menu)

        # Exclude the current instance from the queryset
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("A category with this name already exists in this menu.")

        return data


class MenuRetrieveSerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True)

    class Meta:
        model = Menu
        fields = ['id', 'title', 'description', 'isActive', 'categories']


class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    menu = serializers.HyperlinkedRelatedField(view_name='menu-detail', queryset=Menu.objects.all())
    category = serializers.HyperlinkedRelatedField(view_name='category-detail', queryset=Category.objects.all())
    categoryName = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = MenuItem
        fields = ['url', 'id', 'name', 'description', 'price', 'image', 'menu', 'category', 'categoryName']

    def validate(self, data):
        menu = data.get('menu')
        name = data.get('name')
        category = data.get('category')

        if category.menu != menu:
            raise serializers.ValidationError("The category must belong to the same menu as the menu item.")

        queryset = MenuItem.objects.filter(name=name, menu=menu)

        # Exclude the current instance from the queryset
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("A menu item with this name already exists in this menu.")

        return data
