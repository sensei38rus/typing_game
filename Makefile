.PHONY: install run test clean

install:
	pip install -r requirements.txt

run:
	python src/main.py

test:
	python -m pytest tests/ -v

clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf tests/__pycache__
	rm -rf .pytest_cache

docker-build:
	docker compose build

docker-test:
	docker compose run --rm test

docker-run:
	docker compose run --rm game
