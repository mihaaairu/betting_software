from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Literal
import uuid


class BetInput(BaseModel):
    # This is used to convert event_id to str bc PostgreSQL storing this field like TEXT.
    event_id: str = Field(coerce_numbers_to_str=True)
    price: Decimal = Field(decimal_places=2, gt=0)


class BetOutput(BaseModel):
    bet_id: uuid.UUID = uuid.uuid4()
    state: Literal['WIN', 'LOSE', 'WAIT']


class BetStateInput(BaseModel):
    state: Literal['WIN', 'LOSE']


class NewBetDB(BaseModel):
    bet_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    state: Literal['WIN', 'LOSE', 'WAIT'] = Field(default='WAIT')
    event_id: str
    price: Decimal = Field(decimal_places=2, gt=0)
