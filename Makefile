server:
	python3 manage.py runserver

makemigrations:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate

test:
	coverage run manage.py test

.PHONY: server makemigrations migrate test