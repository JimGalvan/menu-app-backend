from rest_framework import serializers
from django.contrib.auth.models import User

from menu.models import Restaurant, Menu


class UserSerializer(serializers.HyperlinkedModelSerializer):
    restaurants = serializers.HyperlinkedRelatedField(many=True, view_name='restaurant-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'restaurants']


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    restaurant = serializers.HyperlinkedRelatedField(view_name='restaurant-detail', queryset=Restaurant.objects.all())

    class Meta:
        model = Menu
        fields = ['url', 'id', 'name', 'description', 'isActive', 'restaurant']


class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    menus = serializers.HyperlinkedRelatedField(many=True, view_name='menu-detail', read_only=True)

    class Meta:
        model = Restaurant
        fields = ['url', 'id', 'owner', 'name', 'address', 'phone', 'email', 'website', 'description', 'logo', 'menus']
