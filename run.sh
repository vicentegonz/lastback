if [ "$DJANGO_ENV" = "production" ]; then
    exec gunicorn --bind 0.0.0.0:$PORT backend.wsgi --threads=2 --workers=3 --timeout 60 --log-level info
else
    exec gunicorn --bind 0.0.0.0:$PORT backend.wsgi --reload --log-level debug
fi
