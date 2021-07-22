from datetime import datetime, timedelta

from django.http import Http404
from rest_framework import generics, status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from .models import KPI, Event, Product, ServiceIndicator, Store, Zone
from .paginations import EventPagination, KPIServicePagination, ProductPagination
from .serializers import (
    EventSerializer,
    KPISerializer,
    ProductSerializer,
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
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        date = self.request.query_params.get("date")
        if date:
            base = datetime.strptime(date, "%Y-%m-%d")
            events = events.filter(created_at__range=[base, base + timedelta(days=1)])
        elif (not start_date) and end_date:
            base = datetime.strptime(end_date, "%Y-%m-%d")
            events = events.filter(created_at__lt=base + timedelta(days=1))
        elif (not end_date) and start_date:
            base = datetime.strptime(start_date, "%Y-%m-%d")
            events = events.filter(created_at__gte=base)
        elif start_date and end_date:
            events = events.filter(
                created_at__range=[
                    datetime.strptime(start_date, "%Y-%m-%d"),
                    datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1),
                ]
            )
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
            category=self.request.data.get("category"),
            date__day=date.day,
            date__month=date.month,
            date__year=date.year,
        )

    def put(self, request, **kwargs):
        try:
            return self.update(request)
        except KPI.DoesNotExist:
            return self.create(request)


class ListKPI(generics.ListAPIView):
    pagination_class = KPIServicePagination

    def get_object(self):
        try:
            pk = self.kwargs["pk"]
            return Store.objects.get(pk=pk)
        except Store.DoesNotExist as store_no_exist:
            raise Http404 from store_no_exist

    def get(self, request, *args, **kwargs):
        store = self.get_object()
        kpis = KPI.objects.filter(store=store.id).order_by("-id")
        start_date = self.request.query_params.get("start_date", None)
        end_date = self.request.query_params.get("end_date", None)
        date = self.request.query_params.get("date", None)
        if date:
            base = datetime.strptime(date, "%Y-%m-%d")
            kpis = kpis.filter(date__range=[base - timedelta(weeks=1), base])
        elif (not start_date) and end_date:
            base = datetime.strptime(end_date, "%Y-%m-%d")
            kpis = kpis.filter(date__lte=base)
        elif (not end_date) and start_date:
            base = datetime.strptime(start_date, "%Y-%m-%d")
            kpis = kpis.filter(date__gte=base)
        elif start_date and end_date:
            kpis = kpis.filter(
                date__range=[
                    datetime.strptime(start_date, "%Y-%m-%d"),
                    datetime.strptime(end_date, "%Y-%m-%d"),
                ]
            )
        category = self.request.query_params.get("category")
        if category:
            kpis = kpis.filter(category=category)
        page = self.paginate_queryset(kpis)
        serializer = KPISerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


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
            date__day=date.day,
            date__month=date.month,
            date__year=date.year,
        )

    def put(self, request, **kwargs):
        try:
            return self.update(request)
        except ServiceIndicator.DoesNotExist:
            return self.create(request)


class ServiceIndicatorList(generics.ListAPIView):
    pagination_class = KPIServicePagination

    def get_object(self):
        try:
            pk = self.kwargs["pk"]
            return Store.objects.get(pk=pk)
        except Store.DoesNotExist as store_no_exist:
            raise Http404 from store_no_exist

    def get(self, request, *args, **kwargs):
        store = self.get_object()
        services = ServiceIndicator.objects.filter(store=store.id).order_by("-id")
        start_date = self.request.query_params.get("start_date", None)
        end_date = self.request.query_params.get("end_date", None)
        date = self.request.query_params.get("date", None)
        if date:
            base = datetime.strptime(date, "%Y-%m-%d")
            services = services.filter(date__range=[base - timedelta(weeks=1), base])
        elif (not start_date) and end_date:
            base = datetime.strptime(end_date, "%Y-%m-%d")
            services = services.filter(date__lte=base)
        elif (not end_date) and start_date:
            base = datetime.strptime(start_date, "%Y-%m-%d")
            services = services.filter(date__gte=base)
        elif start_date and end_date:
            services = services.filter(
                date__range=[
                    datetime.strptime(start_date, "%Y-%m-%d"),
                    datetime.strptime(end_date, "%Y-%m-%d"),
                ]
            )
        page = self.paginate_queryset(services)
        serializer = ServiceSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class ProductList(generics.ListAPIView):
    pagination_class = ProductPagination

    def get_object(self):
        try:
            pk = self.kwargs["pk"]
            return Store.objects.get(pk=pk)
        except Store.DoesNotExist as store_no_exist:
            raise Http404 from store_no_exist

    def get(self, request, *args, **kwargs):
        store = self.get_object()
        products = Product.objects.filter(stores=store)
        page = self.paginate_queryset(products)
        serializer = ProductSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
