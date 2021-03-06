import json
import os
import random
from typing import List

from fastapi import APIRouter, Depends

from ..models.events import EventBase, CreateEvent
from ..service.eventSvc import EventService

router = APIRouter(
    prefix='/events'
)


@router.get('/all-events', response_model=List[EventBase])
def get_all_events(service: EventService = Depends()):
    return service.get_all_events()


@router.get('/get-event/{event_id}', response_model=EventBase)
def get_event(event_id: str, service: EventService = Depends()):
    return service.get_event(event_id)


@router.post('/add-event', response_model=EventBase)
def create_event(event_data: CreateEvent, service: EventService = Depends()):
    return service.create_event(event_data)


@router.put('/update-event/{event_id}', response_model=EventBase)
def update_event(event_id: str, event_data: CreateEvent, service: EventService = Depends()):
    return service.update_event(event_id, event_data)


@router.delete('/delete-event/{event_id}', response_model=bool)
def delete_event(event_id: str, service: EventService = Depends()):
    return service.delete_event(event_id)
