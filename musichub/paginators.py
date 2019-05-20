from rest_framework import pagination


class DefaultSetPagination(pagination.PageNumberPagination):
    page_size = 20
