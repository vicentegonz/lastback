from datetime import datetime

from django.http import Http404
from rest_framework import generics, status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from .models import KPI, Event, ServiceIndicator, Store, Zone
from .paginations import EventPagination
from .serializers import (
    EventSerializer,
    KPISerializer,
    ServiceSerializer,
    StoreSerializer,
    ZoneSerializer,
)


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


class KPICreate(CreateModelMixin, UpdateModelMixin, generics.GenericAPIView):
    permission_classes = [HasAPIKey]
    serializer_class = KPISerializer

    def get_object(self):
        if not self.request.data.get("date"):
            date = datetime.utcnow()
        else:
            date = datetime.strptime(self.request.data.get("date"), "%Y-%m-%d")
        return KPI.objects.get(
            store=self.request.data.get("store"),
            name=self.request.data.get("name"),
            category=self.request.data.get("category"),
            date__day=date.day,
            date__month=date.month,
            date__year=date.year,
        )

    def put(self, request, **kwargs):
        try:
            return self.partial_update(request)
        except KPI.DoesNotExist:
            return self.create(request)


class ListKPI(APIView):
    @classmethod
    def get_object(cls, pk):
        try:
            return Store.objects.get(pk=pk)
        except Store.DoesNotExist as store_no_exist:
            raise Http404 from store_no_exist

    def get(self, request, pk, *args, **kwargs):
        store = self.get_object(pk)
        kpis = KPI.objects.filter(store=store.id)
        serializer = KPISerializer(kpis, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ServiceIndicatorCreate(
    CreateModelMixin, UpdateModelMixin, generics.GenericAPIView
):
    permission_classes = [HasAPIKey]
    queryset = ServiceIndicator.objects.all()
    serializer_class = ServiceSerializer

    def get_object(self):
        if not self.request.data.get("date"):
            date = datetime.utcnow()
        else:
            date = datetime.strptime(self.request.data.get("date"), "%Y-%m-%d")
        return ServiceIndicator.objects.get(
            store=self.request.data.get("store"),
            name=self.request.data.get("name"),
            date__day=date.day,
            date__month=date.month,
            date__year=date.year,
        )

    def put(self, request, **kwargs):
        try:
            return self.partial_update(request)
        except ServiceIndicator.DoesNotExist:
            return self.create(request)


class ServiceIndicatorList(APIView):
    @classmethod
    def get_object(cls, pk):
        try:
            return Store.objects.get(pk=pk)
        except Store.DoesNotExist as store_no_exist:
            raise Http404 from store_no_exist

    def get(self, request, pk, *args, **kwargs):
        store = self.get_object(pk)
        services = ServiceIndicator.objects.filter(store=store.id)
        serializer = ServiceSerializer(services, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
