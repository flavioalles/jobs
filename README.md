### `jobs`
---
#### Description

An API providing a service that manages job postings.

#### (Software) Architecture

**MVC**. Where:
- Model(s): located at [`src/jobs/models`](src/jobs/models/).
- Controller(s) (or Service(s)): located at [`src/jobs/services`](src/jobs/services/).
- View(s) (or Endpoint(s)): located at [`src/jobs/endpoints`](src/jobs/endpoints/).

#### Models

Four models defined the `jobs` universe.
- `Organization`: a company (or organization).
- `Job`: a job opening posted by an organization.
- `User`: a job hunter.
- `Application`: an application from a user for a job.

The relate to each as such:
- `Organization` : `Job` (`1:n`).
- `Job` : `Application` (`1:n`).
- `User` : `Application` (`1:n`).

#### Endpoints

Check them (and test them) at where you're serving the app and `/docs` (**Swagger UI**) or `/redoc` (**Redocly**).

#### Authentication

`Organization` (or `/organizations`) and `User` (or `/users`) are the authenticated entities of the system.

`OAuth2` with password flow using `JWT` Bearer tokens is used for authenticating. See the endpoints below for a peek at implementation details and the overall flow of the solution:
- `POST /api/v1/organizations/`, `POST /api/v1/organizations/auth` & `POST /api/v1/organizations/<id>/jobs`.
- `POST /api/v1/users/`, `POST /api/v1/users/auth` & `POST /api/v1/users/<id>/applications`.

---
#### Developer Notes

##### Stack

- Programming Language: `Python`.
- Database Engine: `MariaDB`.
- Web (ASGI) Framework: `FastAPI`.
- Testing: `pytest`.
- Dependency Management: `poetry`.

##### Python

- Version used during development: `3.12.4` (i.e. latest stable available at the time).
- Local Environment (i.e. Python Interpreter) managed via `pyenv`.
- Virtual Environment and dependencies installation managed by `poetry`.

##### MariaDB

- Latest supported version by latest SQLAlchemy version is `10.9`.
    - See [this](https://docs.sqlalchemy.org/en/20/dialects/mysql.html) SQLAlchemy doc.
    - To make use of `make` to interface with DB, `docker pull mariadb:10.9.8`.
- DB schema versioning maintained via `alembic`.

##### Workflow

`make` is the interface to most (if not all) tools necessary for development. `make help` lists and (briefly) describes available targets.

```fish
↪ make help
jobs

Available targets:

  install        Installs Python application dependencies (via poetry)
  install-dev    Installs Python app. and dev. dependencies (via poetry)
  check-format   Check code formatting
  format         Format code
  start-db       Start the database container
  stop-db        Stop the database container
  connect-db     Connect to the database
  test           Run tests
  repl           Start an interactive Python shell
  run-dev-app    Run the development version of the application
  run-app        Run the application
```

##### Settings

`Settings` (defined at [`src/jobs/settings/base.py`](src/jobs/settings/base.py)) is the entity representing the available app. configurations.

```python
class Settings(BaseSettings):
    """
    Configuration settings for the jobs API.

    Attributes:
        app_name (str): The name of the application.
        debug (bool): Flag indicating whether debug mode is enabled.
        description (str): A description of the API service.
        database_url (str): The URL of the database.

    """

    app_name: str = "jobs"
    debug: bool = False
    description: str = "An API providing a service that manages job postings."
    database_url: str
    jwt_algorithm: str = "HS256"
    jwt_secret_key: str
    jwt_token_expiration_minutes: int = 60

    class Config:
        env_file = os.getenv("ENV_FILE", None)
```

See also `src/jobs/settings/.env.{development,pytest}` and the `run-dev-app` and/or `run-app` targets in the `Makefile` for an example on how to configure and pass on the configuration to the application.

##### `alembic`

Regular `alembic` workflow used to track DB schema. Hence, root has the usual `alembic` dir. and `alembic.ini`.

Assuming use of `poetry`-managed virtual env., run the command below to generate new revision:

```fish
↪ poetry run alembic revision --autogenerate -m "<Revision description.>"
```

And to upgrade to latest version:

```fish
↪ poetry run alembic upgrade head
```

##### Future Work

- Drop relative in-package imports.
- Proper integration of `mypy` into dev. workflow.
- Containerize application.
- Add caching to reads.
- Create CI actions to run tests, check code formatting, typing hints, etc.