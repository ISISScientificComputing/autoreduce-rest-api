# pylint:skip-file
"""
Wrapper for the functionality for various installation and project setup commands
see:
    `python setup.py help`
for more details
"""
from setuptools import setup, find_packages

setup(name="autoreduce_rest_api",
      version="22.0.0.dev2",
      description="ISIS Autoreduction Runs REST API",
      author="ISIS Autoreduction Team",
      url="https://github.com/ISISScientificComputing/autoreduce/",
      install_requires=[
          "autoreduce_utils==22.0.0.dev3", "autoreduce_scripts==22.0.0.dev11", "django==3.2.4",
          "djangorestframework==3.12.4"
      ],
      packages=find_packages(),
      entry_points={"console_scripts": ["autoreduce-rest-api-manage = autoreduce_rest_api.manage:main"]},
      classifiers=[
          "Programming Language :: Python :: 3 :: Only",
      ])
