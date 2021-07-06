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


def generate_indicator(base, current_date, days, MEAN_VALUES, DESV_VALUES, MIN_VALUES):
    service_indicator = []

    for _ in range(days):
        values = [ random.randint(max(MIN_VALUES[idx],MEAN_VALUES[idx] - 
        DESV_VALUES[idx]),MEAN_VALUES[idx]+DESV_VALUES[idx]) for idx in range(15)]


        for idx in range(2,15,2):
            values[idx] = min(values[0],values[idx])
            if values[idx] == 0:
                values[idx-1]=0

        

        service_indicator.append({
            "amount_of_surveys": values[0],          
            "nps": values[1],
            "amount_nps": values[2],
            "experience": values[3],
            "amount_experience": values[4],
            "kindness": values[5],
            "amount_kindness": values[6],
            "waiting_time": values[7],
            "amount_waiting_time": values[8],
            "speed": values[9],
            "amount_speed": values[10],
            "quality": values[11],
            "amount_quality": values[12],
            "bathroom": values[13],
            "amount_bathroom": values[14],
            "date": current_date.strftime("%Y-%m-%d"),
            **copy.deepcopy(base),
        })

        current_date += timedelta(days=1)

    return service_indicator


def generate_indicators(base, current_date, days, MEAN_VALUES, DESV_VALUES, MIN_VALUES):
    service_indicators = [
        *generate_indicator(
            base,
            current_date,
            days,
            MEAN_VALUES,
            DESV_VALUES,
            MIN_VALUES
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


    MEAN_VALUES = [7,1,2,14,2,14,2,14,2,10,1,10,1,10,1]
    DESV_VALUES= [2,1,2,10,1,10,2,10,2,6,1,6,1,7,1]
    MIN_VALUES= [1,-3,1,1,1,1,0,1,1,1,0,1,0,1,0]

    FIRST_SERVICE_INDICATORS = generate_indicators(
        FIRST_STORE_BASE,
        INITIAL_DATE,
        100,
        MEAN_VALUES,
        DESV_VALUES,
        MIN_VALUES
    )

    SECOND_SERVICE_INDICATORS = [*generate_indicators(
        SECOND_STORE_BASE,
        INITIAL_DATE,
        100,
        MEAN_VALUES,
        DESV_VALUES,
        MIN_VALUES
    )]

    SERVICE_INDICATORS = [*FIRST_SERVICE_INDICATORS, *SECOND_SERVICE_INDICATORS]

    FIXTURES = to_fixtures(SERVICE_INDICATORS, 1, "operations.ServiceIndicator")

    jsonString = json.dumps(FIXTURES, indent=2, sort_keys=False, ensure_ascii=False)
    jsonFile = open("service_indicators.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()