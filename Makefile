.PHONY: initial program setup start_dev

start_dev:
	@echo "Running app in development..."
	uvicorn src.main:app --host 0.0.0.0 --port 8002 --reload

start_prod:
	@echo "Running app in production..."
	gunicorn -w 2 -k uvicorn.workers.UvicornWorker src.main:app -b 0.0.0.0:8002

compose_up:
	@echo "Running docker compose..."
	docker-compose up 

compose_down:
	@echo "Shutting down docker compose..."
	docker-compose down