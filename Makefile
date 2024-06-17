.PHONY: help
help:
	@echo "\033[1;4;32mjobs\033[0m"
	@echo
	@echo "\033[1;4;32mAvailable targets:\033[0m"
	@echo
	@echo "\033[1;32m  install\033[0m        Installs Python application dependencies (via poetry)"
	@echo "\033[1;32m  install-dev\033[0m    Installs Python app. and dev. dependencies (via poetry)"
	@echo "\033[1;32m  check-format\033[0m   Check code formatting"
	@echo "\033[1;32m  format\033[0m         Format code"
	@echo "\033[1;32m  start-db\033[0m       Start the database container"
	@echo "\033[1;32m  stop-db\033[0m        Stop the database container"
	@echo "\033[1;32m  connect-db\033[0m     Connect to the database"
	@echo "\033[1;32m  test\033[0m           Run tests"
	@echo "\033[1;32m  repl\033[0m           Start an interactive Python shell"
	@echo "\033[1;32m  run-dev-app\033[0m    Run the development version of the application"
	@echo "\033[1;32m  run-app\033[0m        Run the application"

.PHONY: install
install:
	@poetry install

.PHONY: install-dev
install-dev:
	@poetry install --with=dev

.PHONY: check-format
check-format:
	@poetry run black --diff --color --target-version=py312 alembic/ src/

.PHONY: format
format:
	@poetry run black --target-version=py312 alembic/ src/

.PHONY: start-db
start-db:
	@docker run --env MARIADB_ROOT_PASSWORD=a-password \
		--name mariadb \
		--publish 3306:3306 \
		--rm \
		--volume ./data/mariadb:/var/lib/mysql \
		mariadb:10.9.8

.PHONY: stop-db
stop-db:
	@docker stop mariadb

.PHONY: connect-db
connect-db:
	@docker exec -i --tty mariadb mysql -u root -p -D jobs

.PHONY: test
test:
	@ENV_FILE=src/jobs/settings/.env.pytest \
		poetry run pytest --cov=src/ --disable-warnings --verbose src/jobs/tests/

.PHONY: repl
repl:
	@poetry run ipython

.PHONY: run-dev-app
run-dev-app:
	@ENV_FILE=src/jobs/settings/.env.development \
		poetry run fastapi dev src/jobs/endpoints/app.py

.PHONY: run-app
run-app:
	@poetry run fastapi run src/jobs/endpoints/app.py