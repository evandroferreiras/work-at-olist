run_dev:
	if python -m flake8 app/.; then\
		export LOCALHOST_DATABASE_URI=postgresql://dev:my-password@localhost:5432/mylocaldb; \
		export FLASK_ENV=development; \
		FLASK_APP=app python -m flask run; \
	else\
		python -m flake8 app/.;\
	fi

test:
	if python -m flake8 app/.; then\
		export FLASK_ENV=test; \
		python -m pytest --pyargs ./tests/ -v; \
	else\
		python -m flake8 app/.;\
	fi

install:
	pip install -r requirements/dev.txt

create_db_dev:
	docker-compose up -d --build

generate_migrate:
	export LOCALHOST_DATABASE_URI=postgresql://dev:my-password@localhost:5432/mylocaldb; \
	export FLASK_ENV=development; \
	FLASK_APP=app/migrate python -m flask db migrate

apply_upgrade_dev:
	export LOCALHOST_DATABASE_URI=postgresql://dev:my-password@localhost:5432/mylocaldb; \
	export FLASK_ENV=development; \
	FLASK_APP=app/migrate python -m flask db upgrade
