from typing import List, Dict

import pymongo
from pymongo import ReturnDocument

from .settings import settings
from .databaseSchema import Event, Player


class EventManipulation:

    def __init__(self):
        self.session = \
            pymongo.MongoClient(settings.database_url, serverSelectionTimeoutMS=5000)['CommanderPairingService']['events']

    def find_one(self, event_id: str) -> dict:
        return self.session.find_one({'Event_id': event_id})

    def find_one_as_object(self, event_id: str) -> Event:
        return Event.decode(self.session.find_one({'Event_id': event_id}))

    def insert_event(self, event: dict):
        self.session.insert_one(event)

    def insert_event_as_object(self, event: Event):
        self.session.insert_one(Event.encode(event))

    def get_all_events(self) -> List[dict]:
        all_events_cursor = self.session.find({})
        return [event for event in all_events_cursor]

    def get_all_events_as_objects(self) -> List[Event]:
        return [Event.decode(event) for event in self.session.find({})]

    def delete_event(self, event_id: str):
        return self.session.find_one_and_delete({'Event_id': event_id})

    def update_event(self, event_id: str, new_values: dict, return_document=ReturnDocument.AFTER) -> dict:
        print('*'*100)
        print(new_values)
        return self.session.find_one_and_update({'Event_id': event_id}, {'$set': new_values},
                                                return_document=return_document)

    def replace_event(self, event_id: str, new_event: dict, return_document=ReturnDocument.AFTER) -> dict:
        return self.session.find_one_and_replace({'Event_id': event_id}, new_event, return_document=return_document)

    def replace_event_as_object(self, event_id: str, new_event: Event, return_document=ReturnDocument.AFTER) -> Event:
        return Event.decode(self.session.find_one_and_replace({'Event_id': event_id}, Event.encode(new_event),
                                                              return_document=return_document))

    def remove_player_from_event(self, event_id: str, player_id: str) -> Event:
        self.session.update({'Event_id': event_id}, {'$pull': {'Players': {'Player_id': player_id}}})
        target_event = Event.decode(self.session.find_one({'Event_id': event_id}))
        return target_event

    def update_player_info(self, event_id: str, player_id: str, player_data: dict) -> Player:
        target_event = self.session.find_one({'Event_id': event_id})
        player_data = dict(player_data)
        target_player = None
        for player in target_event['Players']:
            if player['Player_id'] == player_id:
                target_player = player
                for key, value in player_data.items():
                    player[key] += value
        self.session.find_one_and_replace({'Event_id': event_id}, target_event)
        return Player.decode(target_player)

    def get_player_from_event(self, event_id: str, player_id: str) -> Player:
        event = self.session.find_one({'Event_id': event_id})
        target_player = None
        for player in event.get('Players'):
            if player['Player_id'] == player_id:
                target_player = player
                break
        return target_player

    def get_all_event_players(self, event_id: str):
        event = self.session.find_one({'Event_id': event_id})
        event_players = event.get('Players')
        return event_players
