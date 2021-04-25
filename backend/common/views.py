from django.db import connections
from django.db.migrations.executor import MigrationExecutor
from django.http import HttpResponse


def health_check(request):
    """
    Returns 503 if any database has a migration that has not been executed,
    returns 200 on any other case.
    """
    plans = [
        executor.migration_plan(executor.loader.graph.leaf_nodes())
        for executor in [
            MigrationExecutor(connections[connection_name])
            for connection_name in connections
        ]
    ]
    status = 503 if any(plans) else 200
    return HttpResponse(status=status)
