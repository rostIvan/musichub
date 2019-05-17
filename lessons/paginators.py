from rest_framework import pagination


class LessonSetPagination(pagination.PageNumberPagination):
    page_size = 2
