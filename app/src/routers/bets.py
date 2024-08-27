import uuid
import logging

from typing import List
from fastapi import APIRouter, HTTPException

from models import BetInput, NewBetDB, BetOutput
from database.db_communication import upsert_bet, get_bets
from database import db_connection


bets_router = APIRouter(prefix='/bets')


@bets_router.post('')
async def create_bet(bet: BetInput) -> uuid.UUID:
    """
    Creates a new bet and save it to the database.
    :param bet: JSON with Bet ID and Bet Price.
    :return: Bet ID
    """
    bet = NewBetDB(**bet.model_dump())
    try:
        await upsert_bet(db_connection, bet)
        return bet.bet_id
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail='Failed to place a bet.')


@bets_router.get('')
async def get_all_bets() -> List[BetOutput]:
    """
    Fetch all bets records from database.
    :return: List with bet records in JSON format.
    """
    from main import db_connection
    try:
        return await get_bets(db_connection)
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail='Failed to fetch available bets.')
