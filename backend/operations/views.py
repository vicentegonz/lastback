from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Event, Store, Zone
from .serializers import EventSerializer, StoreSerializer, ZoneSerializer


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

        for store in Store.objects.all():
            # Make call to external Api of recommendation for this store.
            # Create event with this recommendation.
            Event.objects.create(store=store, data={"event": "fake event"})

        events = Event.objects.all()
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
        # Send notification with each event to all the users related to this store.
        serializer = EventSerializer(events, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
