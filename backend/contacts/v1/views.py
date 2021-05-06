from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response


class ContactView(ListAPIView):

    serializer_class = ContactSerializer

    def get_queryset(self):
        role = self.request.query_params.get('role', None)
        if role == 1:
            queryset = ZoneLeaderUser.objects.all()
        else if role == 0:
            queryset = AdminUser.objects.all()
        else:
            queryset = User.objects.all()

        return queryset
        


