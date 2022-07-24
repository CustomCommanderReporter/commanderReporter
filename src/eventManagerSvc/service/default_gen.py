from uuid import uuid4

from eventManagerSvc.models.eventManager import AddPlayerToEvent, DefaultPlayerData


class DefaultPlayerModel:
    @staticmethod
    def gen_default_player_params(self, player_data: AddPlayerToEvent) -> DefaultPlayerData:
        new_player = {'Points': 0,
                      'Sub_points': 0,
                      'Has_autowin': [],
                      'Hidden_points': 0,
                      'Status': False,
                      'Player_id': str(uuid4()),
                      'Player_name': player_data.Player_name,
                      'Commander': player_data.Commander,
                      'Winner': []}
        if player_data.Deck_link:
            new_player['Deck_link'] = player_data.Deck_link
        return new_player
