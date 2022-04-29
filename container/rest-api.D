FROM ghcr.io/autoreduction/base

# Installs rest-api from your local repository
ADD . .
RUN python3 -m pip install --user --no-cache-dir .

CMD ["gunicorn", "--bind", "0.0.0.0:8001", "--workers", "4", "autoreduce_rest_api.autoreduce_django.wsgi"]
