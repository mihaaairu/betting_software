import json

from fastapi import APIRouter, HTTPException

from models import BetStateInput
from database import db_connection
from database.db_communication import update_bets_states, check_event_exits

events_router = APIRouter(prefix='/events')


@events_router.put('/{event_id}')
async def event_update(event_id: str, bet_state: BetStateInput) -> str:
    """
    Updates state for a bulk of rows in database with current event_id.
    """
    if not await check_event_exits(db_connection, event_id):
        raise HTTPException(status_code=400, detail=f'Event [{event_id}] does not exist.')
    await update_bets_states(db_connection, bet_state, event_id)
    return f'Event [{event_id}] new status is [{bet_state.state}]'
