# <REPO_NAME>
<REPO_DESCRIPTION>

Add more information here

## Project layout
* app - The main code for the fastapi server
* codefresh - Directives to codefresh for CI/CD and testing
* deploy - Directives to kubernetes for deployment
* requirements - Python package requirements, managed via pip-compile

## Docker compose
The docker compose file defines 3 services:
* A Postgres server
* An application server with uvicorn
* A test runner

The intention is that the postgres server and application server will be constantly running, and the application server
will auto-restart when changes are made to the codebase. The test runner is started and stopped as needed for running
tests.

# Pre commit hooks
Several pre-commit hooks are defined, and should be installed in the developer's local git checkout using
[pre-commit](https://pre-commit.com/#usage). Staged files that fail the checks in these will be modified (but not
re-staged) and should be reviewed and then manually re-staged for commit (that is, `git add`). Most are basic
formatting/validation, but the `pip-compile` hooks will generate new `requirements.txt` files if the respective
`requirements.in` files have been staged with changes. (See below for details.)

## Python requirement files
This repo uses [pip-compile](https://github.com/jazzband/pip-tools#without-setuppy) to manage dependencies. Application
requirements are listed in `requirements/requirements.in` which is used to generate `requirements/requirements.txt`,
which is what is actually used for installation. Test requirements are listed in `requirements/requirements-test.in`
and both `.in` files are used to generate `requirements/requirements-test.txt`, which is only used for test purposes.
Pre-commit hooks (see above) enforce committing updated `requirements.txt` files when the respective `requirements.in`
files are changed.

## Makefile shortcuts
This project comes with a Makefile with several targets defined for ease of development.

### start
Starts up the <REPO_NAME> application server and Postgres server. Will rebuild the container images and update the
`requirements/requirements.txt` & `requirements/requirements-test.txt` files (if necessary).

### start-detached
Same as [start](#start), but does not output to terminal.

### test
Spins up a new test runner container and runs all tests, or only the tests defined with `make test tests=/path`. Will
also rebuild container images and update the `requirements/requirements.txt` & `requirements/requirements-test.txt`
files (if necessary).

### db-shell
Launches the [psql](https://www.postgresql.org/docs/13/app-psql.html) shell on the Postgres server. Assumes the
Postgres server is currently running.

### python-shell
Launches the python shell on the <REPO_NAME> application server. Assumes the application server is currently running.

### bash-shell
Launches a bash shell on whatever container is passed as `c` (`make bash-shell c=container`). Assumes the container
is currently running.

### pip-compile
Rebuilds `requirements/requirements.txt` & `requirements/requirements-test.txt` if and only if they are older than
one of `requirements/requirements.in` and `requirements/requirements-test.in`

### alembic-revision
Prompts for a migration message and generates a new alembic revision.

### migrate
Applies all existing alembic migrations to the database.
