from typing import List
from datetime import datetime

from databaseSvc.databaseManipulation import DataBaseManipulation
from fastapi import HTTPException, Depends

from eventSvc.models.events import CreateEvent, EventBase
from eventSvc.service.gen_default import GenDefaultEventData


class EventService:
    def __init__(self, session=Depends(DataBaseManipulation)):
        self.session = session

    def get_all_events(self) -> List[EventBase]:
        return self.session.get_all_events()

    def get_event(self, event_id: str) -> dict:
        event = self.session.find_event(event_id)
        if not event:
            raise HTTPException(status_code=404, detail='No event with ID: {event_id}')
        return event

    def create_event(self, event_data: CreateEvent) -> EventBase:
        actual_event_data = self.session.insert_event(GenDefaultEventData(event_data))
        return actual_event_data

    def update_event(self, event_id: str, event_data: CreateEvent) -> dict:
        return self.session.update_event(event_id, event_data)

    def delete_event(self, event_id: str) -> bool:
        return self.session.delete_event(event_id)
