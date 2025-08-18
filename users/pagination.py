from rest_framework.pagination import PageNumberPagination

# class MyCustomPagination(PageNumberPagination):
#     page_size =3
#     page_query_param ='page_size'
#     max_page_size=3


# ______Custom CursorPagination_________
from rest_framework.pagination import CursorPagination
class MyCursorPagination(CursorPagination):
    page_size =3
    ordering = 'date_joined'
    cursor_query_param='cursor'