from datetime import datetime, timedelta

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response


class ListPredictions(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        arn = settings.FORECAST_ARN
        store = self.request.query_params.get("store")
        product = self.request.query_params.get("product")
        start_date = self.request.query_params.get("date")
        session = boto3.Session(region_name="us-east-2")
        forecastquery = session.client(service_name="forecastquery")
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
            data = forecastquery.query_forecast(
                ForecastArn=arn,
                StartDate=start_date + "T00:00:00",
                EndDate=end_date + "T00:00:00",
                Filters={"item_id": product, "location": store},
            )
        except ClientError as error:
            return Response(
                data={"error": str(error)}, status=status.HTTP_502_BAD_GATEWAY
            )
        return Response(data=data["Forecast"]["Predictions"], status=status.HTTP_200_OK)
