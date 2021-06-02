# Main instructions for this template.
1. Press the `use this template` button.
![image](https://user-images.githubusercontent.com/61423717/111556651-aaf13500-8750-11eb-9a7d-1b695020c514.png)
2. Select a name for your new repo.
![image](https://user-images.githubusercontent.com/61423717/111557003-72059000-8751-11eb-82dc-2c8e6ddc3efb.png)
3. Use the `Description` bar to select which framework you will use:
![image](https://user-images.githubusercontent.com/61423717/111557270-f821d680-8751-11eb-989b-7563fe36f8b7.png)
The available options are:
    * django  (**Default**, if none of these options are typed in the description bar, Django will be used)
    * react
    * phoenix
    * fastapi

4. End result. All the files inside of the `./template/$SELECTED_FRAMERWORK` are placed in the root of the repo and
   everything else is deleted. (these screenshots are using Francisco Prin's personal repo)
   ![image](https://user-images.githubusercontent.com/61423717/111558292-1be61c00-8754-11eb-9e70-abaa476476d5.png)
   ![image](https://user-images.githubusercontent.com/61423717/111558322-2dc7bf00-8754-11eb-9c4e-28131534e266.png)
   ![image](https://user-images.githubusercontent.com/61423717/111558363-41732580-8754-11eb-8915-ba9a01a3fff4.png)
   ![image](https://user-images.githubusercontent.com/61423717/111558562-9c0c8180-8754-11eb-9740-09ae4bdb9534.png)

# Specific instructions for the different templates
## Fastapi
This _mostly_ works, and gets 95% of the way to a running fastapi app with postgres & alembric migrations,
but a few steps must be done manually & locally after creating a new repo from the template.

It is assumed that the local development machine has:
- git (obviously)
- python (any of system, pyenv, virtualenv or similar can work)
  - the pip package `pre-commit` installed in the python environment via pip
- make (used to shorten long commands/sequences of commands, handle ordering of actions)

- Install the pre-commit hooks locally with `pre-commit install`
- Run `make repo-init`
  - This will create local images for the application, test runner and postgres, generate
    `requirements/requirements.txt` & `requirements/requirements-test.txt` and create an inital alembic setup.
- Edit the generated `app/migrations/env.py` to include the following snippets:
```
from app.config import settings
```
```
env_psql = context.get_x_argument(as_dictionary=True).get("env_psql", "true")
if env_psql.lower() == "true":
    config.set_main_option("sqlalchemy.url", settings.database.uri)
```

- git add the new files: `alembic.ini`, the contents of `app/migrations` and `requirements/requirements.txt` &
  `requirements/requirements-test.txt`. On commit:
    - The `Fix End of Files` hook will add a newline to the end of `app/migrations/README` and fail.
    - The black hook will restructure a parenthetical in `app/migrations/env.py` and fail.

Git add the changed files and commit again.

Afterwards, run `make start` to build and spin up postgres & fastapi containers.
Go to http://localhost:8080/health-check/ to see the basic health check and verify that the fastapi is up and running.
Run `make test` to spin up a new docker instance with the test requirements installed and run all tests,
or use `make test tests=/path/to/test/file` to run only the tests in a given file.
