from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import OrderingFilter


class CustomPagination(LimitOffsetPagination):
    limit_query_param = 'size'
    offset_query_param = 'start'
