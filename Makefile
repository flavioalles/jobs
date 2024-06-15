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
	@poetry run pytest --verbose src/jobs/tests/