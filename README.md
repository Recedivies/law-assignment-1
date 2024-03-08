# API Gatekeeper Web Service

![PyPI - Format](https://img.shields.io/badge/4.2.9-000000.svg?logo=django&label=django&labelColor=%23092E20&link=https%3A%2F%2Fdocs.djangoproject.com%2Fen%2F4.2%2Freleases%2F4.2%2F)
[![python](https://img.shields.io/badge/Python-3.8-3776AB.svg?style=flat&logo=python&logoColor=white)](https://docs.python.org/3/whatsnew/3.8.html#what-s-new-in-python-3-12)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Setup Development Environment

### Requirements

- pip >= v23.3

### Steps

- Install [pre-commit](https://pre-commit.com/) hook (for linting) using this command after installing the requirements
  in virtual env

```shell
pre-commit install
```

- Create .env file (example in .env.example)

## Setup Database

### Requirements

- PostgreSQL v16

## How to Create an App

```shell
python3 manage.py startapp --template app-template <app-name>
```
