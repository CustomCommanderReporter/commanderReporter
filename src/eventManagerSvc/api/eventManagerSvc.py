from fastapi import APIRouter, Depends
from loguru import logger

from ..models.eventManager import AddPlayerToEvent, FullPlayerData, GeneralEventInfo, TagretPlayerPoints, RoundGenData
from ..service.eventManagerSvc import EventManagerSvc


router = APIRouter(prefix='/event-manager')


@router.get('/get-full-event-data/{event_id}', response_model=GeneralEventInfo)
def get_full_event_data(event_id: str, manager_svc: EventManagerSvc = Depends()):
    output_info = manager_svc.get_full_event_data(event_id)
    return output_info


@router.post('/add-player/{event_id}', response_model=FullPlayerData)
def add_player_to_event(event_id: str, player_data: AddPlayerToEvent, manager_svc: EventManagerSvc = Depends()):
    return manager_svc.add_player_to_event(event_id, player_data)


# TODO: think about this endpoint response model
@router.delete('/remove-player/{event_id}/{player_id}', response_model=GeneralEventInfo)
def remove_player_from_event(event_id: str, player_id: str, manager_svc: EventManagerSvc = Depends()):
    manager_svc.remove_player_from_event(event_id, player_id)
    return manager_svc.get_full_event_data(event_id)


@router.put('/update-player-points/{event_id}/{player_id}', response_model=FullPlayerData)
def update_player_points(event_id: str, player_id: str, round_num: int, player_data: TagretPlayerPoints,
                         manager_svc: EventManagerSvc = Depends()):
    update_response = manager_svc.update_player_points(event_id, player_id, round_num, player_data)
    return update_response


@router.put('/generate-round/{event_id}', response_model=RoundGenData)
def generate_round(event_id: str, round_number: int, manager_svc: EventManagerSvc = Depends()):
    target_round = manager_svc.generate_round(event_id, round_number)
    return target_round


# TODO: think about optimizing this endpoint response
# Looks like we can make more complex processing on frontend and avoid full event data in response
@router.put('/change-event-player/{event_id}/{player_id}', response_model=GeneralEventInfo)
def update_player_on_event(event_id: str, player_id: str, player_data: AddPlayerToEvent,
                           manager_svc: EventManagerSvc = Depends()):
    manager_svc.update_player_on_event(event_id, player_id, player_data)
    return manager_svc.get_event_player(event_id, player_id)


# TODO: same as upper
@router.delete('/remove-player-from-event/{event_id}/{player_id}')
def remove_player_from_event(event_id: str, player_id: str, manager_svc: EventManagerSvc = Depends()):
    manager_svc.remove_player_from_event(event_id, player_id)
    return manager_svc.get_full_event_data(event_id)


@router.post('/change-event-state/{event_id}', response_model=GeneralEventInfo)
def change_event_state(event_id: str, target_state: str, manager_svc: EventManagerSvc = Depends()):
    return manager_svc.change_event_state(event_id, target_state)
