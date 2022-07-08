from typing import List, Union
from datetime import datetime
from pydantic import BaseModel


class AddPlayerToEvent(BaseModel):
    Player_name: str
    Commander: str
    Deck_link: Union[str, None]


class DefaultPlayerData():
    Points: int
    Sub_points: int
    Has_autowin: int
    Hidden_points: float
    Status: bool
    Player_id: str
    Commander: str


class PlayerOnTable(BaseModel):
    name: str
    id: str


class UpdatePlayerResponse:
    status: bool
    player_data: PlayerOnTable


class Table(BaseModel):
    Table_num: int
    Table_players: List[PlayerOnTable]


class Round(BaseModel):
    Number: int
    Players_on_table: List[Table]


class PlayerInfo(AddPlayerToEvent):
    Player_id: str
    Player_name: str
    Commander: str
    Deck_link: Union[str, None]
    Points: int
    Sub_points: int
    Hidden_points: float
    Status: bool

class BaseEvenForPlayer(BaseModel):
    Event_id: str
    player_data: AddPlayerToEvent


class PlayerBase(BaseModel):
    Player_id: int
    Player_name: str
    Commander: str
    Deck_link: str
    Points: int
    Sub_points: int
    Has_autowin: bool


class UpdatePlayerPoints(BaseModel):
    Points: int
    Sub_points: int


class GeneralEventInfo(BaseModel):
    Event_id: str
    Event_name: str
    Event_Date: datetime
    Players: List[PlayerInfo]
    Rounds: Union[List[Round], None]
    Status: str
