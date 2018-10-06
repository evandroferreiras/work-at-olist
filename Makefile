run_dev:
	if flake8 app/.; then\
		export FLASK_ENV=development && FLASK_APP=app flask run; \
	else\
		flake8 app/.;\
	fi

test:
	if flake8 app/.; then\
		pytest --pyargs ./tests/ -v; \
	else\
		flake8 app/.;\
	fi

install:
	pip install -r requirements/dev.txt
