from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class EventPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "size"
    max_page_size = 15

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.page.paginator.count,
                "results": data,
                "status": status.HTTP_200_OK,
            }
        )


class KPIPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "size"
    max_page_size = 15

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.page.paginator.count,
                "results": data,
                "status": status.HTTP_200_OK,
            }
        )


class ProductPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "size"
    max_page_size = 15

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.page.paginator.count,
                "results": data,
                "status": status.HTTP_200_OK,
            }
        )
