from databases import Database
from models import NewBetDB, BetOutput, BetStateInput
from typing import List
from asyncpg import Record


async def upsert_bet(database: Database, bet: NewBetDB) -> None:
    query = """
        INSERT INTO bets (bet_id, event_id, price, state)
        VALUES (:bet_id, :event_id, :price, :state)
        ON CONFLICT (bet_id) 
        DO UPDATE
        SET
            event_id = EXCLUDED.event_id,
            price = EXCLUDED.price,
            state = EXCLUDED.state
    """
    return await database.execute(query, bet.model_dump())


async def update_bets_states(database: Database, state: BetStateInput, event_id) -> None:
    query = f"""
        UPDATE bets
        SET state = '{state.state}'
        WHERE event_id = '{event_id}';
    """

    return await database.execute(query)


async def get_bets(database: Database) -> List[str]:
    raw_data = await database.fetch_all(query=f"SELECT bet_id, state FROM bets")
    return [BetOutput(**dict(row)).model_dump_json() for row in raw_data]


async def check_event_exits(database: Database, event_id: str | int) -> Record | None:  # Just for UX
    query = f"""
        SELECT 1
        FROM bets
        WHERE event_id = '{event_id}'
        LIMIT 1
    """
    return await database.fetch_one(query)
