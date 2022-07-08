import random
import time
from copy import copy, deepcopy
from operator import itemgetter
from uuid import uuid4

from fastapi import Depends, HTTPException, Response, Body
from loguru import logger

from databaseSvc.databaseManipulation import DataBaseManipulation

from eventManagerSvc.models.eventManager import AddPlayerToEvent, UpdatePlayerResponse
from eventManagerSvc.service.default_gen import DefaultPlayerModel


class EventManagerSvc:
    def __init__(self, session=Depends(DataBaseManipulation)):
        self.session = session

    def gen_player_hidden_points(self, turn_postition: int, round_number: int, points: int, sub_points: int) -> float:
        """
            This is only my fantasies, we need to discuss this thing. This is only template for calculating points.
            Now used basic standings generation. Sort by points than by tiebreaks
            turn_position is now unreacheable parameter
        """
        position_coefficient = 1 + (turn_postition / 10)
        round_coefficient = 1 + round_number / 10 if round_number > 1 else 1
        logger.debug(position_coefficient)
        logger.debug(round_coefficient)
        logger.debug((points * position_coefficient * round_coefficient) + sub_points / 15)
        return points + (sub_points / 10)         

    def get_full_event_data(self, event_id: str) -> dict:
        target_event = self.session.find_event(event_id)
        if not target_event:
            raise HTTPException(status_code=404,
                                details={'status': False, 'details': f'Not found event {event_id}'})
        return target_event

    def get_event_player(self, event_id: str, player_id: str) -> dict:
        target_player = self.session.find_player_on_event(event_id, player_id)
        if not target_player:
            raise HTTPException(status_code=404,
                                details={'status': False,
                                         'details': f'Player {player_id} not found on {event_id}'})
        return target_player

    def change_event_state(self, event_id: str, target_state: str) -> dict:
        try:
            self.session.update_event(event_id, {'Status': target_state})
        except Exception as e:
            # TODO: catch target exceptions
            raise HTTPException(status_code=500,
                                details={'status': False,
                                         'details': f'Error while change event state: {e}'})
        return self.session.find_event(event_id)

    def update_player_on_event(self, event_id: str, player_id: str, player_data: dict) -> UpdatePlayerResponse:
        player = self.get_event_player(event_id, player_id)
        if not player:
            raise HTTPException(status_code=404, details={'status': False, 'details': player_data})
        player_data = dict(player_data)
        for target_key in player_data:
            if not player.get(target_key):
                raise HTTPException(status_code=502,
                                    details={'status': False,
                                             'details': f'player_id: {player_id}; Not found fields: {target_key};'})
            player[target_key] = player_data[target_key]
        try:
            self.session.update_player(event_id, player_id, dict(player))
            self.session.update_player_on_table(event_id, player_id, player_data['Player_name'])
        except Exception as e:
            # TODO: find exceptions to catch
            raise HTTPException(status_code=500, details={'status': False, 'details': 'Player data was not updated in db'})
        return {'status': True, 'player_data': player_data}

    def add_player_to_event(self, event_id: str, player_data: AddPlayerToEvent) -> dict:
        target_event = self.session.find_event(event_id)
        if not target_event:
            raise HTTPException(status_code=404,
                                details={'status': False,
                                         'details': f'Not found event {event_id}'})
        target_player_data = DefaultPlayerModel.gen_default_player_params(player_data)
        if target_event.get('Players'):
            target_event['Players'].append(target_player_data)
        else:
            target_event['Players'] = [target_player_data]
        # TODO: Rework this thing. Replacing event to add player looks like shit
        try:
            self.session.replace_event(event_id, target_event)
        except Exception as e:
            raise HTTPException(status_code=500, details={'status': False,
                                                          'details': f'Cant update event in db;\n{player_data}'})
        return target_player_data

    # TODO: look at this thing additional time and improve test coverage starting from this!
    def remove_player_from_event(self, event_id: str, player_id: str) -> dict:
        event = self.session.find_event(event_id)
        if not event:
            raise HTTPException(status_code=404, details={'status': False, 'details': f'Not found event {event_id}'})
        if event['Status'] == 'created':
            # TODO: catch exception
            return self.session.update_event(event_id,
                                             {'Players': {'Player_id': player_id}},
                                             operation='$pull')
        elif event['Status'] == 'Started':
            target_player = self.session.find_player_on_event(event_id, player_id).get('Players')[0]
            target_player['Status'] = True
            return self.session.update_player(event_id,
                                              player_id,
                                              target_player)
        elif event['Status'] == 'finished':
            return {'error': 'Event already finished'}  # Change this to http exception
        else:
            # TODO: check statuscode
            return HTTPException(status_code=500,
                                 details={'status': False,
                                          'details': 'Unknown event status'})

    # TODO: this method needs MAJOR refactoring. Check database interractions and improve it
    def update_player_points(self, event_id: str, player_id: str, round_number: int, player_data: dict):
        try:
            target_player = self.session.find_player_on_event(event_id, player_id).get('Players')
        except Exception as e:
            # TODO: catch exceptions not Exception
            raise HTTPException(error_code=500, details={'status': False, 'details': f'Error while find player in db {e}'})
        if not target_player[0]:
            raise HTTPException(error_code=404,
                                details={'status': False,
                                         'details': 'On event {event_id} not found {player_id}'})
        target_event_rounds = self.session.find_event(event_id).get('Rounds')
        if not target_event_rounds:
            raise HTTPException(error_code=404, details={'status': False, 'details': 'Not found Rounds in {event_id}'})
        target_table = None
        for event_round in target_event_rounds:
            if event_round['Number'] == round_number:
                for table in event_round['Players_on_table']:
                    if player_id in [t_id['id'] for t_id in table['Table_players']]:
                        target_table = table
        if target_table:
            table_players = [player['id'] for player in target_table['Table_players']]
            logger.debug(table_players)
            player_turn_pos = table_players.index(target_player['Player_id'])+1
        else:
            player_turn_pos = 1
        target_player['Points'] += int(player_data.Points)
        target_player['Sub_points'] += int(player_data.Sub_points)
        player_hidden_points = self.gen_player_hidden_points(player_turn_pos,
                                                             round_number,
                                                             int(player_data.Points),
                                                             int(player_data.Sub_points))
        if target_player.get('Hidden_points'):
            target_player['Hidden_points'] += player_hidden_points
        else:
            target_player['Hidden_points'] = player_hidden_points
        return self.session.update_player(event_id, player_id, target_player)

    # TODO: look at this method additional times. It also looks bad
    def generate_round(self, event_id: str, round_number: int):
        target_event = self.session.find_event(event_id)
        target_players_data = [{'name': player['Player_name'],
                                'id': player['Player_id'],
                                'Hidden_points': player['Hidden_points']} for player in target_event['Players'] if not player['Status']]
        random.seed(33)
        if round_number == 1:
            for _ in range(5):
                random.shuffle(target_players_data)
        else:
            target_players_data = sorted(target_players_data, key=itemgetter('Hidden_points'), reverse=True)
        players_on_tables = [target_players_data[i:i + 4] for i in range(0, len(target_players_data), 4)]
        # Give buys to players
        # Need to update and generate rounds using this parameter.
        # TODO: update response of this method and return also players with buys
        players_to_tables = deepcopy(players_on_tables)
        if len(players_on_tables[-1]) < 3:
            for player in players_on_tables[-1]:
                player['Has_autowin'] = 3
                self.session.update_player(event_id, player['id'], player)
            players_to_tables = players_on_tables[:-1]
        [random.shuffle(table) for table in players_to_tables]
        tables_data = [{'Table_num': table_num+1, 'Table_players': players_to_tables[table_num]} for table_num in range(len(players_to_tables))]
        if target_event.get('Rounds'):
            target_event['Rounds'].append({'Number': round_number,
                                           'Players_on_table': tables_data})
        else:
            target_event['Rounds'] = [{'Number': round_number,
                                       'Players_on_table': tables_data}]
        return self.session.update_event(event_id, target_event)
        
