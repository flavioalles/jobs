.PHONY: check-format
check-format:
	@poetry run black --diff --color --target-version=py312 src/ tests/

.PHONY: format
format:
	@poetry run black --target-version=py312 src/ tests/