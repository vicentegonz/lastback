from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Device
from .serializers import DeviceSerializer, UserSerializer


class UserDetail(APIView):
    def get(self, request, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeviceListView(CreateModelMixin, UpdateModelMixin, GenericAPIView):
    serializer_class = DeviceSerializer

    def get_object(self):
        android_id = self.request.data.get("android_id")
        ios_id = self.request.data.get("ios_id")

        return Device.objects.get(android_id=android_id, ios_id=ios_id)

    def put(self, request, **kwargs):
        request.data["user"] = request.user.id

        try:
            return self.partial_update(request)
        except Device.DoesNotExist:
            return self.create(request)
