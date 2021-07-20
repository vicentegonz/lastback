import csv
from datetime import datetime, timedelta

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from backend.operations.models import Event, Store
from backend.operations.serializers import EventSerializer


class ListPredictions(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        store = self.request.query_params.get("store")
        product = self.request.query_params.get("product")
        start_date = self.request.query_params.get("date")
        if not (store and product and start_date):
            data = {}
            if not store:
                data["store"] = ["This field is requiered"]
            if not product:
                data["product"] = ["This field is requiered"]
            if not start_date:
                data["date"] = ["This field is requiered"]
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        date1 = datetime.strptime(start_date, "%Y-%m-%d")
        date2 = date1 + timedelta(days=7)
        end_date = date2.strftime("%Y-%m-%d")

        try:
            data = forecast_prediction(
                start_date + "T00:00:00", end_date + "T00:00:00", product, store
            )
        except ClientError as error:
            return Response(
                data={"error": str(error)}, status=status.HTTP_502_BAD_GATEWAY
            )
        return Response(data=data["Forecast"]["Predictions"], status=status.HTTP_200_OK)


def forecast_prediction(start_date, end_date, product_id, store_id):
    arn = settings.FORECAST_ARN
    session = boto3.Session(region_name="us-east-2")
    forecastquery = session.client(service_name="forecastquery")
    return forecastquery.query_forecast(
        ForecastArn=arn,
        StartDate=start_date,
        EndDate=end_date,
        Filters={"item_id": product_id, "location": store_id},
    )


class CreateRecommendation(APIView):
    permission_classes = [HasAPIKey]

    def post(self, request, *args, **kwargs):

        date = self.request.data.get("date")
        if not date:
            end_date = datetime.now()
        else:
            end_date = datetime.strptime(date, "%Y-%m-%d")
        start_date = end_date - timedelta(days=7)

        events = []
        for store in Store.objects.all():
            data = {}
            for product in store.products.all():

                try:
                    data_end_date = forecast_prediction(
                        end_date.strftime("%Y-%m-%d") + "T00:00:00",
                        end_date.strftime("%Y-%m-%d") + "T00:00:00",
                        str(product.id),
                        str(store.id),
                    )

                    value_end_date = data_end_date["Forecast"]["Predictions"]["mean"][
                        0
                    ]["Value"]
                    value_start_date = day_data(start_date, store.id, product.id)
                    if not value_start_date:
                        continue

                    diff = 0.1
                    if value_end_date > value_start_date * (diff + 1):
                        data[product.description] = (
                            "Se estima que "
                            + f"se venderá {diff*100}% más que la semana anterior"
                        )
                    elif value_end_date < value_start_date * (1 - diff):
                        data[product.description] = (
                            "Se estima que "
                            + f"se venderá {diff*100}% menos que la semana anterior"
                        )

                except ClientError:
                    continue
            if data:
                events.append(Event.objects.create(store=store, data=data))

        return Response(
            data=EventSerializer(events, many=True).data, status=status.HTTP_201_CREATED
        )


def get_weekly():
    s3 = boto3.resource("s3")
    bucket = s3.Bucket("arcoprime.example.data")

    obj = list(bucket.objects.filter(Prefix="Datos Formato CSV/weekly"))[0]

    body = obj.get()["Body"].read()

    data = body.decode("utf-8")

    lines = data.splitlines()
    reader = csv.reader(lines)

    return reader


def day_data(date, store_id, product_id):
    data = get_weekly()
    next(data)

    for line in data:
        if datetime.strptime(line[1], "%Y-%m-%d") == date:
            if int(line[3]) == store_id and int(line[0]) == product_id:
                return int(line[2])

    return 0
