.PHONY: check-format
check-format:
	@poetry run black --diff --color --target-version=py312 src/ tests/

.PHONY: format
format:
	@poetry run black --target-version=py312 src/ tests/

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