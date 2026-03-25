install:
	uv sync
	uv run pre-commit install -f

update: install
	uv sync --upgrade
	uv run pre-commit autoupdate

checks: install
	uv run pre-commit run --all-files

tests: install
	uv run pytest --cov=loom --cov-report=term-missing

lint:
	skip=pytest uv run pre-commit run

clean:
	@rm -rf .venv
	@rm -rf build dist *.egg-info
	@rm -rf logs
	@find loom -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find loom -type f -name "*.pyc" -delete
	@find loom -type f -name "*.pyo" -delete
	@find loom -type f -name "*.so" -delete
	@find loom -type f -name "*.c" -delete
	@rm -rf .pytest_cache .coverage

compile:
	@rm -rf build dist *.egg-info
	@uv run --no-dev python scripts/cythonizer.py

container:
	docker buildx build -t loom:latest .
	docker image prune -f
