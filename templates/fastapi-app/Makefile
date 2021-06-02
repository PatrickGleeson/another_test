# Various shortcuts for common dev tasks

start: build
	# To start the a local instance of the fastapi server and postgres DB
	docker-compose up <REPO_NAME>

start-detached: build
	# To start the a local instance of the fastapi server and postgres DB in a detached state (i.e. backgrounded)
	docker-compose up -d <REPO_NAME>

test: build
	docker-compose run <REPO_NAME>-test-runner 'python wait_for_postgres.py && pytest ${tests}'

db-shell:
	# Postgres db shell
	docker-compose exec postgres bash -c 'psql --username $$POSTGRES_USER $$POSTGRES_DB'

python-shell:
	# Python shell on <REPO_NAME>'s app container
	docker-compose exec <REPO_NAME> python

bash-shell:
	# bash shell on c=<container_name>
	docker-compose exec ${c} bash

pip-compile: requirements/requirements.txt requirements/requirements-test.txt


MIGRATION_MESSAGE ?= $(shell bash -c 'read -p "Migration Message: " msg; echo $$msg')
alembic-revision:
	# Generate a new alembic revision
	docker-compose run <REPO_NAME> bash -c 'alembic revision --autogenerate -m "${MIGRATION_MESSAGE}"'

migrate:
	# Apply all alembic migrations
	docker-compose run <REPO_NAME> bash -c 'alembic upgrade head'

repo-init: build
	# Only use on initial setup of the repo
	docker-compose run <REPO_NAME> bash -c 'alembic init app/migrations'

# Intermediate steps

build: requirements/requirements.txt requirements/requirements-test.txt
	docker-compose build

requirements/requirements.txt requirements/requirements-test.txt &: requirements/requirements.in requirements/requirements-test.in
	# Generates new requirements.txt files if the requirements.in files are out of date
	pre-commit run pip-compile --files requirements/requirements.in requirements/requirements-test.in

.PHONY: start, test, db-shell, python-shell, bash-shell, pip-compile alembic-revision, migrate, build
