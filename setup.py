# pylint:skip-file
"""
Wrapper for the functionality for various installation and project setup commands
see:
    `python setup.py help`
for more details
"""
from setuptools import setup, find_packages

setup(name="autoreduce_rest_api",
      version="22.0.0.dev1",
      description="ISIS Autoreduction Runs REST API",
      author="ISIS Autoreduction Team",
      url="https://github.com/ISISScientificComputing/autoreduce/",
      install_requires=[
          "autoreduce_db==22.0.0.dev3", "autoreduce_utils==22.0.0.dev2", "django==3.2.4", "django_rest_framework"
      ],
      packages=find_packages(),
      entry_points={"console_scripts": ["autoreduce-qp-start = autoreduce_qp.queue_processor.queue_listener:main"]},
      classifiers=[
          "Programming Language :: Python :: 3 :: Only",
      ])
