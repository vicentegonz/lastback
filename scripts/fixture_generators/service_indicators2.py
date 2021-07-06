import copy
import json
import random
from datetime import datetime, timedelta


def to_fixtures(data, initial_id, model_name):
    fixtures = []
    for index in range(0, len(data)):
        fixtures.append({
            "model": model_name,
            "pk": initial_id + index,
            "fields": data[index],
        })
    return fixtures


def generate_indicator(base, current_date, days):
    service_indicator = []

    for _ in range(days):
        nps = random.randint(-5, 20)
        values = [random.randint(0, 150) for _ in range(6)]
        surveys = random.randint(0,25)
        amount_values = [random.randint(0, surveys+1) for idx in range(7)]

        service_indicator.append({
            "nps": nps,
            "amount_nps": amount_values[0],
            "experience": values[0],
            "amount_experience": amount_values[1],
            "kindness": values[1],
            "amount_kindness": amount_values[2],
            "waiting_time": values[2],
            "amount_waiting_time": amount_values[3],
            "speed": values[3],
            "amount_speed": amount_values[4],
            "quality": values[4],
            "amount_quality": amount_values[5],
            "bathroom": values[5],
            "amount_bathroom": amount_values[6],
            "amount_of_surveys": surveys,
            "date": current_date.strftime("%Y-%m-%d"),
            **copy.deepcopy(base),
        })

        current_date += timedelta(days=1)

    return service_indicator


def generate_indicators(base, current_date, days):
    service_indicators = [
        *generate_indicator(
            base,
            current_date,
            days
        ),
    ]

    return service_indicators


if __name__ == "__main__":
    FIRST_STORE_BASE = {
        "store_id": 2088,
        "created_at": "2021-06-07T10:30:00.998Z",
        "updated_at": "2021-06-07T10:30:00.998Z",
    }

    SECOND_STORE_BASE = {
        "store_id": 2047,
        "created_at": "2021-06-07T10:30:00.998Z",
        "updated_at": "2021-06-07T10:30:00.998Z",
    }

    INITIAL_DATE = datetime.strptime("2021-06-01", "%Y-%m-%d")



    FIRST_SERVICE_INDICATORS = generate_indicators(
        FIRST_STORE_BASE,
        INITIAL_DATE,
        100
    )

    SECOND_SERVICE_INDICATORS = [*generate_indicators(
        SECOND_STORE_BASE,
        INITIAL_DATE,
        100
    )]

    SERVICE_INDICATORS = [*FIRST_SERVICE_INDICATORS, *SECOND_SERVICE_INDICATORS]

    FIXTURES = to_fixtures(SERVICE_INDICATORS, 1, "operations.ServiceIndicator")

    jsonString = json.dumps(FIXTURES, indent=2, sort_keys=False, ensure_ascii=False)
    jsonFile = open("service_indicators.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()