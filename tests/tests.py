import pytest
import uuid
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from main import app

event_id = 'some_event_id'
zero_event_id = 'some_nonexistent_event_id'
price = 123.45
state = 'WIN'


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_create_bet(anyio_backend):
    data = {
        'event_id': event_id,
        'price': price
    }

    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://localhost") as ac:
            response = await ac.post("/bets", json=data)
        assert response.status_code == 200, f"Status code {response.status_code} != 200"

        assert isinstance(uuid.UUID(response.json()), uuid.UUID), "Response JSON is not a valid UUID"


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_all_bets(anyio_backend):
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://localhost") as ac:
            response = await ac.get("/bets")
        assert response.status_code == 200, f"Status code {response.status_code} != 200"

        response_json = response.json()
        assert isinstance(response_json, list), "Response JSON is not a valid list"

        for item in response_json:
            assert isinstance(item, dict), f"Item {item} is not a valid dict"

            assert 'bet_id' in item, f"Item {item} does not contain 'bet_id' field"
            assert 'state' in item, f"Item {item} does not contain 'state' field"

            assert isinstance(uuid.UUID(item['bet_id']), uuid.UUID), f"Field 'bet_id' in {item} is not a valid UUID"
            assert item['state'] in ['WIN', 'LOSE', 'WAIT'], f"Field 'state' in {item} is not a valid state"


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_event_update(anyio_backend):
    data = {
        'state': state
    }

    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://localhost") as ac:
            response = await ac.put(f"/events/{event_id}", json=data)
        assert response.status_code == 200, f"Status code {response.status_code} != 200"
        assert response.json() == f'Event [{event_id}] new status is [{state}]'


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_event_update_nonexistent_event(anyio_backend):
    data = {
        "state": state
    }

    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://localhost") as ac:
            response = await ac.put(f"/events/{zero_event_id}", json=data)
        assert response.status_code == 400, f"Status code {response.status_code} != 400"
        assert response.json() == {'detail': 'Event [some_nonexistent_event_id] does not exist.'}
