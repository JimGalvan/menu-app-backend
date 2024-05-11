from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from menu.permissions import IsOwnerOrReadOnly
from menu.models import Menu, Category, MenuItem
from menu.serializers import UserSerializer, MenuSerializer, CategorySerializer, \
    MenuItemSerializer, MenuRetrieveSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


from rest_framework.response import Response
from rest_framework.decorators import action


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MenuRetrieveSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def menu_items(self, request, pk=None):
        menu = self.get_object()
        menu_items = MenuItem.objects.filter(menu=menu)
        serializer = MenuItemSerializer(menu_items, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def categories(self, request, pk=None):
        menu = self.get_object()
        categories = Category.objects.filter(menu=menu)
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
