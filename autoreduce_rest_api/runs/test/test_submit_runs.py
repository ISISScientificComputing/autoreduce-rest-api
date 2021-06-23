import requests


def test_some_run():
    requests.post("http://127.0.0.1:8000/api/submit/run/MARI/28034")
