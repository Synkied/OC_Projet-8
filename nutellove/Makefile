init:
	pip install -r requirements.txt

create_db:
	createdb -U $(u) $(n)

migrate_db:
	python manage.py makemigrations
	python manage.py migrate

feed_db:
	python db_feeding.py

cover_test:
	coverage run manage.py test

cov_report:
	coverage report