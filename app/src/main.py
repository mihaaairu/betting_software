import json
import logging
import os
import uuid

from fastapi import FastAPI, HTTPException
from typing import List
from databases import Database
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from models import BetInput, BetStateInput, NewBetDB
from logger import set_logger
from db_api import upsert_bet, get_bets, update_bets_states, check_event_exits

load_dotenv()
set_logger(std_level=logging.DEBUG, enable_std_exceptions=True)


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


database = Database(os.environ['PG_URL'])

app = FastAPI(lifespan=lifespan)


@app.post('/bets')
async def create_bet(bet: BetInput) -> uuid.UUID:
    """
    Creates a new bet and save it to the database.
    :param bet: JSON with Bet ID and Bet Price.
    :return: Bet ID
    """
    bet = NewBetDB(**bet.model_dump())
    try:
        await upsert_bet(database, bet)
        return bet.bet_id
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail='Failed to place a bet.')


@app.get('/bets')
async def get_all_bets() -> List[str]:
    """
    Fetch all bets records from database.
    :return: List with bet records in JSON format.
    """
    try:
        return await get_bets(database)
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail='Failed to fetch available bets.')


@app.put('/events/{event_id}')
async def event_update(event_id: str, bet_state: BetStateInput) -> str:
    """
    Updates state for a bulk of rows in database with current event_id.
    """
    if not await check_event_exits(database, event_id):
        raise HTTPException(status_code=400, detail=f'Event [{event_id}] does not exist.')
    await update_bets_states(database, bet_state, event_id)
    return json.dumps(f'Event [{event_id}] new status is [{bet_state.state}]')
