install-local:
	python -m pip install -r requirements/local.txt

install-prod:
	python -m pip install -r requirements.txt

migrate:
	python manage.py makemigrations
	python manage.py migrate

fixtures:
	python manage.py loaddata admin

test:
	coverage run --source='.' manage.py test
	coverage report

update:
	make install-local
	make migrate

run-psql:
	docker start psql

exec-psql:
	docker exec -it psql bash
