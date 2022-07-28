FROM ghcr.io/autoreduction/base

# Installs rest-api from your local repository
ADD . .
RUN python3 -m pip install --user --no-cache-dir .

CMD ["autoreduce-rest-api-manage", "serve", "--port", "8004"]
