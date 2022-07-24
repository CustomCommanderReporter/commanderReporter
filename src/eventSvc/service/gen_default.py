from datetime import datetime

from uuid import uuid4


class GenDefaultEventData:
    @staticmethod
    def gen_default_event_data(event_data: dict):
        actual_event_data = event_data.dict()
        actual_event_data['Status'] = 'created'
        actual_event_data['Event_id'] = str(uuid4())
        actual_event_data['Rounds'] = []
        actual_event_data['Players'] = []
        actual_event_data['Event_Date'] = str(datetime.strptime(actual_event_data['Event_Date'], '%d %B, %Y'))
        return actual_event_data
