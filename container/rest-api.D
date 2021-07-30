FROM autoreduction/base

ADD ./setup.py /autoreduce-rest-api/setup.py

# add --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple for packages in test.pypi.org
RUN python3 -m pip install --no-cache-dir gunicorn autoreduce-rest-api==22.0.0.dev7

CMD autoreduce-rest-api-manage runserver 8000
