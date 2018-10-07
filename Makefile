run_dev:
	if flake8 app/.; then\
		export LOCALHOST_DATABASE_URI=postgresql://dev:my-password@localhost:5432/mylocaldb; \
		export FLASK_ENV=development; \
		FLASK_APP=app flask run; \
	else\
		flake8 app/.;\
	fi

test:
	if flake8 app/.; then\
		export FLASK_ENV=test; \
		pytest --pyargs ./tests/ -v; \
	else\
		flake8 app/.;\
	fi

install:
	pip install -r requirements/dev.txt

create_db_dev:
	docker-compose up -d --build

generate_migrate:
	export LOCALHOST_DATABASE_URI=postgresql://dev:my-password@localhost:5432/mylocaldb; \
	export FLASK_ENV=development; \
	FLASK_APP=app/migrate flask db migrate

apply_upgrade_dev:
	export LOCALHOST_DATABASE_URI=postgresql://dev:my-password@localhost:5432/mylocaldb; \
	export FLASK_ENV=development; \
	FLASK_APP=app/migrate flask db upgrade
