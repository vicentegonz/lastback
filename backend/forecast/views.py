import csv
from datetime import datetime, timedelta

import boto3
import pytz
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
        forecastclient = boto3.client("forecast", region_name="us-east-2")

        if not (store and product and start_date):
            data = {}
            if not store:
                data["store"] = ["This field is requiered"]
            if not product:
                data["product"] = ["This field is requiered"]
            if not start_date:
                data["date"] = ["This field is requiered"]
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        current_date = datetime.strptime(start_date, "%Y-%m-%d")
        current_sunday = current_date + timedelta(days=(6 - current_date.weekday()))

        try:

            forecast_data = forecast_prediction(
                current_date.strftime("%Y-%m-%d") + "T00:00:00",
                current_sunday.strftime("%Y-%m-%d") + "T00:00:00",
                product,
                store,
                get_forecast_arns(
                    settings.DATASETGROUP_ARN,
                    forecastclient,
                )[0],
            )

            next_week_forecast_data = forecast_prediction(
                (current_sunday + timedelta(days=1)).strftime("%Y-%m-%d") + "T00:00:00",
                (current_date + timedelta(days=7)).strftime("%Y-%m-%d") + "T00:00:00",
                product,
                store,
                get_forecast_arns(
                    settings.DATASETGROUP_ARN,
                    forecastclient,
                )[1],
            )

            for metric in forecast_data["Forecast"]["Predictions"].keys():
                forecast_data["Forecast"]["Predictions"][
                    metric
                ] += next_week_forecast_data["Forecast"]["Predictions"][metric]

        except ClientError as error:
            return Response(
                data={"error": str(error)}, status=status.HTTP_502_BAD_GATEWAY
            )

        return Response(
            data=forecast_data["Forecast"]["Predictions"], status=status.HTTP_200_OK
        )


class CreateRecommendation(APIView):
    permission_classes = [HasAPIKey]

    def post(self, request, *args, **kwargs):

        current_date = (
            datetime.strptime(self.request.data.get("date"), "%Y-%m-%d")
            if self.request.data.get("date")
            else datetime.strptime(
                datetime.now(pytz.timezone("America/Santiago"))
                .date()
                .strftime("%Y-%m-%d"),
                "%Y-%m-%d",
            )
        )  # Fecha de Santiago

        events = []

        current_sunday = current_date + timedelta(days=(6 - current_date.weekday()))

        for store in Store.objects.all():
            data = {}
            for product in store.products.all():
                try:
                    forecast_data = forecast_prediction(
                        current_date.strftime("%Y-%m-%d") + "T00:00:00",
                        current_sunday.strftime("%Y-%m-%d") + "T00:00:00",
                        str(product.id),
                        str(store.id),
                        get_forecast_arns(
                            settings.DATASETGROUP_ARN,
                            boto3.client("forecast", region_name="us-east-2"),
                        )[0],
                    )

                    next_week_forecast_data = forecast_prediction(
                        (current_sunday + timedelta(days=1)).strftime("%Y-%m-%d")
                        + "T00:00:00",
                        (current_date + timedelta(days=7)).strftime("%Y-%m-%d")
                        + "T00:00:00",
                        str(product.id),
                        str(store.id),
                        get_forecast_arns(
                            settings.DATASETGROUP_ARN,
                            boto3.client("forecast", region_name="us-east-2"),
                        )[1],
                    )

                    for metric in forecast_data["Forecast"]["Predictions"].keys():
                        forecast_data["Forecast"]["Predictions"][
                            metric
                        ] += next_week_forecast_data["Forecast"]["Predictions"][metric]

                    historical_data = weekly_data(
                        [
                            (
                                (current_date - timedelta(days=7)) + timedelta(day)
                            ).strftime("%Y-%m-%d")
                            for day in range(7)
                        ],
                        store.id,
                        product.id,
                        get_weekly(),
                    )

                    process_historical_data(
                        historical_data, forecast_data, product, data
                    )

                except ClientError:
                    continue

            process_data(data, events, store)

        return Response(
            data=EventSerializer(events, many=True).data, status=status.HTTP_201_CREATED
        )


def process_data(data, events, store):
    found = False
    delete_keys = []
    for day in data:
        if data[day]:
            found = True
        else:
            delete_keys.append(day)
    for key in delete_keys:
        data.pop(key)
    if found:
        events.append(Event.objects.create(store=store, data=data))


def process_historical_data(historical_data, forecast_data, product, data):
    for time_object in forecast_data["Forecast"]["Predictions"]["mean"]:
        timestamp = time_object["Timestamp"].split("T")[0]
        timestamp_prev = (
            datetime.strptime(timestamp, "%Y-%m-%d") - timedelta(days=7)
        ).strftime("%Y-%m-%d")
        if timestamp_prev in historical_data:
            forecast = time_object["Value"]
            historical = historical_data[timestamp_prev]

            if timestamp not in data:
                data[timestamp] = {}
            diff = 0.1
            if forecast > historical * (diff + 1):
                data[timestamp][product.description] = (
                    "Se estima que "
                    f"se venderá {diff*100}% más que el "
                    "mismo día "
                    "de la semana anterior"
                )
            elif forecast < historical * (1 - diff):
                data[timestamp][product.description] = (
                    "Se estima que "
                    f"se venderá {diff*100}% menos que el "
                    "mismo día "
                    "de la semana anterior"
                )


def get_weekly():
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(settings.S3_BUCKET)

    try:
        obj = list(bucket.objects.filter(Prefix=settings.S3_BUCKET_ROUTE))[0]
    except IndexError as error:
        return Response(data={"error": str(error)}, status=status.HTTP_502_BAD_GATEWAY)

    body = obj.get()["Body"].read()

    data = body.decode("utf-8")

    lines = data.splitlines()
    reader = csv.reader(lines)
    next(reader)

    return list(reader)


def weekly_data(dates, store_id, product_id, historical_data):
    data = {}
    for line in historical_data:
        date = line[1]
        if date in dates:
            if int(line[3]) == store_id and int(line[0]) == product_id:
                data[date] = float(line[2])
    return data


def forecast_prediction(start_date, end_date, product_id, store_id, arn):

    session = boto3.Session(region_name="us-east-2")
    forecastquery = session.client(service_name="forecastquery")

    return forecastquery.query_forecast(
        ForecastArn=arn,
        StartDate=start_date,
        EndDate=end_date,
        Filters={"item_id": product_id, "location": store_id},
    )


def get_forecast_arns(datasetgroup_arn, forecast):
    filters = [
        {"Condition": "IS", "Key": "Status", "Value": "ACTIVE"},
        {"Condition": "IS", "Key": "DatasetGroupArn", "Value": datasetgroup_arn},
    ]
    paginator = forecast.get_paginator("list_forecasts")
    response = paginator.paginate(
        PaginationConfig={
            "MaxItems": 100,
            "PageSize": 100,
            "StartingToken": None,
        },
        Filters=filters,
    )
    next_creation_date = datetime(2020, 1, 1)
    current_arn, next_arn = "", ""
    for page in response:
        for forecast_object in page["Forecasts"]:
            if (next_arn == "") or (
                next_creation_date < forecast_object["CreationTime"]
            ):
                current_arn = next_arn
                next_arn = forecast_object["ForecastArn"]
                next_creation_date = forecast_object["CreationTime"]
            else:
                current_arn = forecast_object["ForecastArn"]
    return current_arn, next_arn
