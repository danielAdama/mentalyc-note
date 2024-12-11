from fastapi import FastAPI
import asyncio
from config.db_config import sessionmanager
from contextlib import asynccontextmanager
import threading
from src.external_services.train_service import TrainPropertyService
from config.kafka_client import KafkaClient
from dotenv import load_dotenv, find_dotenv
from config.logger import Logger
logger = Logger(__name__)

_ = load_dotenv(find_dotenv())

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    try:
        sessionmanager.init()
        logger.info(f"Initized Async PostgresqlDB Successfully")

        # Initialize KafkaClient and TrainPropertyService
        kafka_client = KafkaClient(["test-train-status"])

        # Run Kafka consumer as an asyncio task
        kafka_task = TrainPropertyService(sessionmanager, kafka_client)
        app.state.kafka_task = asyncio.create_task(kafka_task.run())
        logger.info("Kafka consumer started listening to test-train-status")

        yield
    finally:
        # Gracefully shutdown the Kafka consumer task
        if hasattr(app.state, 'kafka_task'):
            app.state.kafka_task.cancel()
            try:
                await app.state.kafka_task
            except asyncio.CancelledError:
                logger.info("Kafka consumer task was cancelled")

        await sessionmanager.close()
        logger.info(f"Async PostgresqlDB shutting down Successfully")