from rest_framework import serializers
from django.contrib.auth.models import User

from menu.models import Restaurant, Menu, Category, MenuItem


class UserSerializer(serializers.HyperlinkedModelSerializer):
    restaurants = serializers.HyperlinkedRelatedField(many=True, view_name='restaurant'
                                                                           '-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'restaurants']


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    restaurant = serializers.HyperlinkedRelatedField(view_name='restaurant-detail', queryset=Restaurant.objects.all())

    class Meta:
        model = Menu
        fields = ['url', 'id', 'name', 'description', 'isActive', 'restaurant', 'categories']


class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    menus = serializers.HyperlinkedRelatedField(many=True, view_name='menu-detail', read_only=True)

    class Meta:
        model = Restaurant
        fields = ['url', 'id', 'owner', 'name', 'address', 'phone', 'email', 'website', 'description', 'logo', 'menus']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    menu = serializers.HyperlinkedRelatedField(view_name='menu-detail', queryset=Menu.objects.all())

    class Meta:
        model = Category
        fields = ['url', 'id', 'name', 'description', 'menu']


def get_category_names(obj):
    return [category.name for category in obj.categories.all()]


class CategoryNameUrlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['url', 'name']


class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # categories = serializers.HyperlinkedRelatedField(many=True, view_name='category-detail',
    #                                                  queryset=Category.objects.all(), required=False)
    categories = CategoryNameUrlSerializer(many=True, read_only=True)
    category_names = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = ['url', 'id', 'owner', 'name', 'description', 'price', 'image', 'categories', 'category_names']

    def get_category_names(self, obj):
        return [category.name for category in obj.categories.all()]
