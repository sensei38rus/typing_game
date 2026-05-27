.PHONY: install run test clean

install:
	pip install -r requirements.txt

run:
	python main.py

test:
	pytest tests/ -v

clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf tests/__pycache__
	rm -rf .pytest_cache