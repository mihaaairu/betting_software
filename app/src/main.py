import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from utils.logger import set_logger
from routers.bets import bets_router
from routers.events import events_router
from database import db_connection


set_logger(std_level=logging.DEBUG, enable_std_exceptions=True)


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await db_connection.connect()
    yield
    await db_connection.disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(bets_router)
app.include_router(events_router)
