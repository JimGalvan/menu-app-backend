from rest_framework.pagination import LimitOffsetPagination


class CustomPagination(LimitOffsetPagination):
    limit_query_param = 'size'
    offset_query_param = 'start'
