from typing import List
from uuid import uuid4
import uuid
from datetime import datetime

from databaseSvc.databaseManipulation import DataBaseManipulation
from fastapi import HTTPException, Depends

from ..models.events import CreateEvent


class EventService:
    def __init__(self, session=Depends(DataBaseManipulation)):
        self.session = session

    # TODO: update and parse time for better output
    def get_all_events(self) -> List[dict]:
        return self.session.get_all_events()

    def get_event(self, event_id: str) -> dict:
        event = self.session.find_event(event_id)
        if not event:
            raise HTTPException(status_code=404, detail='No event with ID: {event_id}')
        return event

    def create_event(self, event_data: CreateEvent) -> dict:
        actual_event_data = event_data.dict()
        actual_event_data['Status'] = 'created'
        actual_event_data['Event_id'] = str(uuid4())
        actual_event_data['Rounds'] = []
        actual_event_data['Event_Date'] = str(datetime.strptime(actual_event_data['Event_Date'], '%d %B, %Y'))
        self.session.insert_event(actual_event_data)
        return actual_event_data

    def update_event(self, event_id: str, event_data: CreateEvent) -> dict:
        return self.session.update_event(event_id, event_data)

    def delete_event(self, event_id: str) -> bool:
        return self.session.delete_event(event_id)
