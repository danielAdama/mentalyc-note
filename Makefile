.PHONY: initial program setup start_dev

start_dev:
	@echo "Running app in development..."
	uvicorn src.main:app --host 0.0.0.0 --port 8020 --reload

start_prod:
	@echo "Running app in production..."
	gunicorn -w 2 -k uvicorn.workers.UvicornWorker src.main:app -b 0.0.0.0:8020

run_test:
	@echo "Running tests..."
	cd src && python3 -m unittest discover tests