web: gunicorn --chdir portfolio_site portfolio_site.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 60
release: python portfolio_site/manage.py migrate --noinput
