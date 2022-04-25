FROM ghcr.io/autoreduction/base

# Installs rest-api from your local repository
ADD . .
RUN python3 -m pip install --user --no-cache-dir .

# Uncomment below if you want to install from pypi
# add --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple for packages in test.pypi.org
# RUN python3 -m pip install --user --no-cache-dir autoreduce-rest-api==22.0.0.dev20

ENTRYPOINT ["/usr/local/bin/dumb-init", "--"]
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "--workers", "4", "autoreduce_rest_api.autoreduce_django.wsgi"]
