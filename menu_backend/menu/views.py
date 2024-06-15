from django.contrib.auth import authenticate
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from menu.models import Menu, Category, MenuItem
from menu.pagination import CustomPagination
from menu.serializers import UserSerializer, MenuSerializer, CategorySerializer, \
    MenuItemSerializer, MenuRetrieveSerializer


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
class BaseViewSet(viewsets.ModelViewSet):
    filter_backends = [OrderingFilter]
    pagination_class = CustomPagination
    ordering_fields = ['createdAt', 'modifiedAt']


class FiltersBaseViewSet(BaseViewSet):

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', None)

        if search_query:
            queryset = queryset.annotate(
                similarity=TrigramSimilarity('name', search_query)
            ).filter(
                Q(description__icontains=search_query) |
                Q(name__icontains=search_query)
            ).order_by('-similarity')

        return queryset


class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'])
    def menus(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        menus = Menu.objects.filter(owner=user)

        # Create a pagination instance
        paginator = PageNumberPagination()

        # Paginate the queryset
        paginated_menus = paginator.paginate_queryset(menus, request)

        serializer = MenuSerializer(paginated_menus, many=True, context={'request': request})

        # Return the paginated response
        return paginator.get_paginated_response(serializer.data)


class MenuViewSet(BaseViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    ordering_fields = ['menu_items__category__name', 'menu_items__price', 'menu_items__name',
                       'menu_items__description']

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

        # Apply search filter
        search_query = self.request.GET.get('search', None)
        if search_query:
            menu_items = menu_items.annotate(
                similarity=TrigramSimilarity('name', search_query)
            ).filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query) |
                Q(price__icontains=search_query)
            ).order_by('-similarity')

        # Apply ordering
        ordering = self.request.query_params.get('ordering')
        if ordering:
            menu_items = menu_items.order_by(ordering)

        # Apply pagination
        paginator = CustomPagination()
        paginated_menu_items = paginator.paginate_queryset(menu_items, request)

        serializer = MenuItemSerializer(paginated_menu_items, many=True, context={'request': request})

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)

    @action(detail=True, methods=['get'])
    def categories(self, request, pk=None):
        menu = self.get_object()
        categories = Category.objects.filter(menu=menu)
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def menu_items(self, request, pk=None):
        category = self.get_object()
        menu_items = MenuItem.objects.filter(category=category)
        serializer = MenuItemSerializer(menu_items, many=True, context={'request': request})
        return Response(serializer.data)


class MenuItemViewSet(BaseViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
