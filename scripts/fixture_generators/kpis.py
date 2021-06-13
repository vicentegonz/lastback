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


def generate_data(base, current_date, transactions, days):
    kpis = []

    for _ in range(days):
        transactions = random.randint(max(0, transactions - 35), transactions + 45)

        base_alimentation_transactions = int(transactions * random.uniform(0.4, 0.7))
        remaining_transactions = transactions - base_alimentation_transactions

        menu_transactions = int(remaining_transactions * random.uniform(0.3, 0.8))
        sandwich_transactions = remaining_transactions - menu_transactions

        # Alimentación Básica
        base_alimentation_items_per_transaction = random.uniform(1, 5)
        base_alimentation_price_per_item = random.randint(2000, 15000)
        base_alimentation_sold_items = int(
            base_alimentation_transactions * base_alimentation_items_per_transaction
        )

        # # Cantidad de transacciones
        kpis.append({
            "name": "Cantidad de transacciones",
            "value": base_alimentation_transactions,
            "category": "Alimentación Básica",
            "date": current_date.strftime("%Y-%m-%d"),
            **copy.deepcopy(base),
        })

        # # Cantidad de ítems vendidos
        kpis.append({
            "name": "Cantidad de ítems vendidos",
            "value": base_alimentation_sold_items,
            "category": "Alimentación Básica",
            "date": current_date.strftime("%Y-%m-%d"),
            **copy.deepcopy(base),
        })

        # # Ventas Totales
        kpis.append({
            "name": "Ventas Totales",
            "value": base_alimentation_sold_items * base_alimentation_price_per_item,
            "category": "Alimentación Básica",
            "date": current_date.strftime("%Y-%m-%d"),
            **copy.deepcopy(base),
        })

        # Sandwich Preparado
        sandwich_items_per_transaction = random.uniform(1, 5)
        sandwich_price_per_item = random.randint(2000, 15000)
        sandwich_sold_items = int(
            sandwich_transactions * sandwich_items_per_transaction
        )

        # # Cantidad de transacciones
        kpis.append({
            "name": "Cantidad de transacciones",
            "value": sandwich_transactions,
            "category": "Sandwich Preparado",
            "date": current_date.strftime("%Y-%m-%d"),
            **copy.deepcopy(base),
        })

        # # Cantidad de ítems vendidos
        kpis.append({
            "name": "Cantidad de ítems vendidos",
            "value": sandwich_sold_items,
            "category": "Sandwich Preparado",
            "date": current_date.strftime("%Y-%m-%d"),
            **copy.deepcopy(base),
        })

        # # Ventas Totales
        kpis.append({
            "name": "Ventas Totales",
            "value": sandwich_sold_items * sandwich_price_per_item,
            "category": "Sandwich Preparado",
            "date": current_date.strftime("%Y-%m-%d"),
            **copy.deepcopy(base),
        })

        # Menú
        menu_items_per_transaction = random.uniform(1, 5)
        menu_price_per_item = random.randint(2000, 15000)
        menu_sold_items = int(
            menu_transactions * menu_items_per_transaction
        )

        # # Cantidad de transacciones
        kpis.append({
            "name": "Cantidad de transacciones",
            "value": menu_transactions,
            "category": "Menú",
            "date": current_date.strftime("%Y-%m-%d"),
            **copy.deepcopy(base),
        })

        # # Cantidad de ítems vendidos
        kpis.append({
            "name": "Cantidad de ítems vendidos",
            "value": menu_sold_items,
            "category": "Menú",
            "date": current_date.strftime("%Y-%m-%d"),
            **copy.deepcopy(base),
        })

        # # Ventas Totales
        kpis.append({
            "name": "Ventas Totales",
            "value": menu_sold_items * menu_price_per_item,
            "category": "Menú",
            "date": current_date.strftime("%Y-%m-%d"),
            **copy.deepcopy(base),
        })

        current_date += timedelta(days=1)

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

    INITIAL_DATE = datetime.strptime("2021-06-01", "%Y-%m-%d")

    FIRST_KPIS = generate_data(FIRST_STORE_BASE, INITIAL_DATE, 500, 100)

    SECOND_KPIS = generate_data(SECOND_STORE_BASE, INITIAL_DATE, 230, 100)

    KPIS = [*FIRST_KPIS, *SECOND_KPIS]

    FIXTURES = to_fixtures(KPIS, 1, "operations.KPI")

    print(json.dumps(FIXTURES, indent=2, sort_keys=False, ensure_ascii=False))
