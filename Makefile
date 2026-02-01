# Postgress Docker Compose commands
docker-up:
	docker compose -f ./dockercompose.yml up -d
docker-down:
	docker compose -f ./dockercompose.yml down

# Format and type checking
check_format:
	@echo "Checking format..."
	uv run ruff check src scripts && uv tool run ruff format --check src scripts

check_type:
	@echo "Checking types..."
	uv run mypy --package db_learn

format:
	@echo "Formatting code..."
	uv tool run ruff check --fix src scripts && uv tool run ruff format src scripts