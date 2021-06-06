from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from .models import KPI, Event, Store, Zone
from .paginations import EventPagination
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


class ListEvents(generics.ListAPIView):
    pagination_class = EventPagination

    def get_object(self):
        try:
            pk = self.kwargs["pk"]
            return Store.objects.get(pk=pk)
        except Store.DoesNotExist as store_no_exist:
            raise Http404 from store_no_exist

    def get(self, request, *args, **kwargs):
        store = self.get_object()
        events = Event.objects.filter(store_id=store.id).order_by("-id")
        page = self.paginate_queryset(events)
        serializer = EventSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class KPICreate(generics.CreateAPIView):
    permission_classes = [HasAPIKey]
    queryset = KPI.objects.all()
    serializer_class = KPISerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)
