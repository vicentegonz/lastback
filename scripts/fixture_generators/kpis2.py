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


def generate_indicator(base, current_date, days, categories):
    kpis = []

    for _ in range(days):
        venta_neta = 0
        contribucion = 0
        transacciones = 0
        venta_bruta = 0
        
        for category in categories[1:]:
            if category.strip() == "Cigarrillos":
                gross_sale = random.randint(1000000,3000000)
                net_sale = random.randint(gross_sale-300000,gross_sale)
                contribution= random.randint(50000,200000)
                transactions =  random.randint(100,500)
            elif category == "Comida":
                gross_sale = random.randint(800000,2000000)
                net_sale = random.randint(gross_sale-200000,gross_sale)
                contribution= random.randint(500000,1000000)
                transactions =  random.randint(100,300)
            elif category == "Cooler":
                gross_sale = random.randint(500000,2500000)
                net_sale = random.randint(gross_sale-200000,gross_sale)
                contribution= random.randint(100000,800000)
                transactions =  random.randint(100,800)
            elif category == "Retail":
                gross_sale = random.randint(300000,1500000)
                net_sale = random.randint(gross_sale-100000,gross_sale)
                contribution= random.randint(50000,500000)
                transactions =  random.randint(50,800)
            elif category == "Cafeteria":
                gross_sale = random.randint(300000,1500000)
                net_sale = random.randint(gross_sale-100000,gross_sale)
                contribution= random.randint(100000,1000000)
                transactions =  random.randint(50,700)
            elif category == "Serv_Comis":
                gross_sale = random.randint(50000,1000000)
                net_sale = random.randint(gross_sale-10000,gross_sale)
                contribution= random.randint(50000,1000000)
                transactions =  random.randint(1,200)
            elif category == "Servicios":
                gross_sale = random.randint(-200000,200000)
                net_sale = random.randint(gross_sale-20000,gross_sale)
                contribution= random.randint(-100000,200000)
                transactions =  random.randint(1,200)
            elif category == "Baños":
                gross_sale = random.randint(1,20000)
                net_sale = random.randint(gross_sale-1000,gross_sale)
                contribution= random.randint(1,20000)
                transactions =  random.randint(1,50)
            elif category == "Dif_varias":
                gross_sale = random.randint(1000,50000)
                net_sale = random.randint(gross_sale-500,gross_sale)
                contribution= random.randint(1,10000)
                transactions =  random.randint(1,20)
            kpis.append({
            "category": category,
            "net_sale": net_sale,
            "contribution": contribution,
            "transactions": transactions,
            "gross_sale": gross_sale,
            "date": current_date.strftime("%Y-%m-%d"),
            **copy.deepcopy(base),
            })
            venta_neta += net_sale
            contribucion += contribution
            transacciones += transactions
            venta_bruta += gross_sale
        kpis.append({
        "category": "TOTAL",
        "net_sale": venta_neta,
        "contribution": contribucion,
        "transactions": transacciones,
        "gross_sale": venta_bruta,
        "date": current_date.strftime("%Y-%m-%d"),
        **copy.deepcopy(base),
        })
        
            

        current_date += timedelta(days=1)

    return kpis


def generate_indicators(base, current_date, days, categories):

    kpis = generate_indicator(
            base,
            current_date,
            days,
            categories
        )

    return kpis


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

    INITIAL_DATE = datetime.strptime("2021-07-05", "%Y-%m-%d")

    KPI_CATEGORIES = [
        "Total", "Cigarrillos", "Comida", "Cooler", "Retail", "Cafeteria", 
        "Serv_Comis", "Servicios", "Baños", "Dif_varias"
    ]


    FIRST_KPIS = generate_indicators(
        FIRST_STORE_BASE,
        INITIAL_DATE,
        40,
        KPI_CATEGORIES
    )

    SECOND_KPIS = generate_indicators(
        SECOND_STORE_BASE,
        INITIAL_DATE,
        40,
        KPI_CATEGORIES
    )

    KPIS = [*FIRST_KPIS, *SECOND_KPIS]

    FIXTURES = to_fixtures(KPIS, 1, "operations.KPI")

    jsonString = json.dumps(FIXTURES, indent=2, sort_keys=False, ensure_ascii=False)
    jsonFile = open("kpis.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()