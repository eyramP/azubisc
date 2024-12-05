from rest_framework.pagination import PageNumberPagination


class AzubiPagination(PageNumberPagination):
    page_size = 50
