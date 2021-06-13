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


def generate_indicator(base, name, current_date, surveys, grade, days):
    service_indicator = []

    for _ in range(days):
        grade = min(max(0, grade + random.uniform(-0.6, 0.8)), 7)
        surveys = random.randint(max(5, surveys - 7), surveys + 15)

        service_indicator.append({
            "name": name,
            "value": round(grade, 2),
            "amount_of_surveys": surveys,
            "date": current_date.strftime("%Y-%m-%d"),
            **copy.deepcopy(base),
        })

        current_date += timedelta(days=1)

    return service_indicator


def generate_indicators(base, names, current_date, surveys, grades, days):
    service_indicators = []

    for index, name in enumerate(names):
        service_indicators = [
            *service_indicators,
            *generate_indicator(
                base,
                name,
                current_date,
                surveys[index],
                grades[index],
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

    INDICATORS_NAMES = [
        "Baños", "Cajeros", "Atención", "Calidad", "Seguridad", "Precios"
    ]

    FIRST_SERVICE_INDICATORS = generate_indicators(
        FIRST_STORE_BASE,
        INDICATORS_NAMES,
        INITIAL_DATE,
        [40, 46, 79, 52, 35, 66],
        [4.3, 5.7, 4.7, 4.5, 3.8, 5.3],
        100
    )

    SECOND_SERVICE_INDICATORS = [*generate_indicators(
        SECOND_STORE_BASE,
        INDICATORS_NAMES,
        INITIAL_DATE,
        [23, 37, 55, 41, 29, 58],
        [5.6, 4.4, 6.1, 5.9, 5.8, 4.3],
        100
    )]

    SERVICE_INDICATORS = [*FIRST_SERVICE_INDICATORS, *SECOND_SERVICE_INDICATORS]

    FIXTURES = to_fixtures(SERVICE_INDICATORS, 1, "operations.ServiceIndicator")

    print(json.dumps(FIXTURES, indent=2, sort_keys=False, ensure_ascii=False))
