FROM ghcr.io/autoreduction/base

ADD ./setup.py /autoreduce-rest-api/setup.py

# add --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple for packages in test.pypi.org
RUN python3 -m pip install --no-cache-dir gunicorn autoreduce-rest-api==22.0.0.dev13

CMD gunicorn --workers 4 -b 0.0.0.0:8000 autoreduce_rest_api.autoreduce_django.wsgi
