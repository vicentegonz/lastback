from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from .models import KPI, Event, Store, Zone
from .serializers import EventSerializer, KPISerializer, StoreSerializer, ZoneSerializer


class StoreList(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class StoreDetail(generics.RetrieveAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class ZoneList(generics.ListAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer


class ZoneDetail(generics.RetrieveAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer


class CreateEvents(APIView):
    def post(self, request, *args, **kwargs):
        # Make call to external Api of recommendation for this store.
        # Create event with this recommendation.
        events = [
            Event.objects.create(store=store, data={"event": "Sample event content"})
            for store in Store.objects.all()
        ]

        serializer = EventSerializer(events, many=True)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ListEvents(APIView):
    @classmethod
    def get_object(cls, pk):
        try:
            return Store.objects.get(pk=pk)
        except Store.DoesNotExist as store_no_exist:
            raise Http404 from store_no_exist

    def get(self, request, pk, *args, **kwargs):
        store = self.get_object(pk)
        events = Event.objects.filter(store_id=store.id)
        serializer = EventSerializer(events, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class KPICreate(generics.CreateAPIView):
    permission_classes = [HasAPIKey]
    serializer_class = KPISerializer
    queryset = KPI.objects.all()
