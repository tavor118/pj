# PJ - Python Junior

Project to store the questions and answers for interview.


# Table of Contents
* [Global Development Requirements](#Global-Development-Requirements)
* [Running and working with the app locally](#Running-and-working-with-the-app-locally)
* [Testing](#Testing)
* [Project structure](#Project-structure)
* [Initial setup](#Initial-setup)
	* [Setup Database](#Setup-Database)
	* [Add pre-commit hooks](#Add-pre-commit-hooks)
	* [Run pre-commit hooks](#Run-pre-commit-hooks)
* [Docker](#Docker)
* [Other](#Other)



## Global Development Requirements

- Python 3.11
- Django >= 4.0
- Postgresql >= 14.5
- Docker and docker-compose (optional)



## Running and working with the app locally

Instead of the standard runserver manage command (`./manage.py runserver`) you can use

```shell
(venv) $ ./manage.py runserver_plus
```

to run the app. This will enhance the server with the Werkzeug interactive
debugger that will allow you to interact with your code (debug it) in the
browser, when it throws an exception instead of returning a valid response.

Similarly, instead of `./manage shell` you can use

```shell
(venv) $ ./manage.py shell_plus
```

and have your models (and a few frequently needed classes and modules) will be
automatically imported.



## Testing

`pytest` used for tests.
Check https://djangostars.com/blog/django-pytest-testing/ article if not familiar.

Use following command to run tests before commit
(With this call, pytest will spawn a number of workers processes equal
to the number of available CPUs, and distribute the tests randomly across them):

```shell
pytest -n auto
```

Or during development:

```shell
pytest -s -vv --no-migrations --reuse-db --tb=short
```
Explanation (some flags used in `pytest.ini`):
- `-s` - don't capture output. By default pytest captures standard output while running tests.
- `-vv` - increases the verbosity level. Or use `-v`
  It’s only if a test fails that it shows the captured output.
- `--no-migrations`: This flag is specific to Django projects. It disables the execution of database migrations during testing.
- `--reuse-db` - after the test run, the test database will not be removed.
- `--tb=short` - sets the level of detail for the displayed traceback output when a test fails. In this case, short is the value specified. It provides a shorter traceback with only the most relevant information about the failure.

Optional:
- `--disable-warnings` - to disable warnings during the tests.
- `--sw` - run tests in `stepwise` move.
  The test suite will run until the first failure and then stop.
  At the next invocation, tests will continue from the last failing test
  and then run until the next failing test.

**Caveat:** If there were updates in the database, with you need to specify `--create-db`
flag to update database with the last changes.



## Project structure

```
.
├── .github/ - github actions
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── src/ - source directory
│   ├── apps/ - applications with business logic
│   ├── settings/ - project settings
│   ├── api_urls.py
│   └── urls.py
├── tests/
│   ├── apps/ - tests for apps
│   └── conftest.py - file with fixtures
├── .env.example - file with environment varialbes
├── Dockerfile
├── README.md
├── docker-compose.yml
├── manage.py
├── pyproject.toml
└── pytest.ini
```



## Initial setup

- Clone the project
- Create an env dir and activate

```shell
python3.11 -m venv venv
source venv/bin/activate
```

- Install requirements.txt
```shell
(venv) $ pip install -r requirements/dev.txt
```

- Setup `.env` file. Copy and rename `.env.example` -> `.env` and fill with proper values.
Check `django-environ` for details.


### Setup Database

Override database configs in your `.env` file if necessary.
postgres command to setup the DB

```shell
psql
#: CREATE DATABASE pythonjunior WITH OWNER postgres;
```
Before being able to run the project, you'll at least have to set up the database.
(Remember, local settings go into the local.py file.) PostgreSQL is the db used
for production, and multiple PostgreSQL-specific extensions are used.

After setting up the db, you should run

```shell
(venv) $ ./manage.py migrate
```


### Add pre-commit hooks

```shell
pre-commit install
```

This will enable black, flake8 and default pre-commit hooks such as end-of-file-fixer.


### Run pre-commit hooks

This command will format all changed files properly and also highlight problematic places

```shell
pre-commit
```
Then add any changed files to commit and try committing the changes.


## Docker

Docker and docker-compose also available
```shell
docker-compose build
docker-compose up
```
or
```shell
docker-compose up --build
```


## Other

- Update TOC in the `README.md` file ([details](https://github.com/alexander-lee/markdown-github-bear-toc))
```shell
markdown-toc -h 3 -t github README.md
```
