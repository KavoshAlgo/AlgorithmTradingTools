from streaming.src.stream_producer import StreamProducer
from monitoring.src.logger import Logger
from enums.event_types import EventTypes
from events.event_manager import EventManager
from events.event import Event


class BrokerService:
    def __init__(self, algorithm_request_channel: str, event_manager_obj: EventManager):

        self.logger = Logger(False, '')
        self.stream_producer = StreamProducer()
        self.producer_topic = algorithm_request_channel
        self.event_manager_obj = event_manager_obj

    async def send_order(self, **kwargs):
        return await self.do_job("send_order", **kwargs)

    async def cancel_order(self, **kwargs):
        return await self.do_job("cancel_order", **kwargs)

    async def edit_order(self, **kwargs):
        return await self.do_job("edit_order", **kwargs)

    async def do_job(self, job, **kwargs) -> Event:
        event_id = self.event_manager_obj.generate_event_id()
        event = await self.event_manager_obj.get_new_event(
            event_type=EventTypes.ALGORITHM_REQUEST_EVENT,
            event_topic=EventTypes.ALGORITHM_REQUEST_EVENT + event_id,
            event_id=event_id)
        self.stream_producer.send(self.producer_topic, {
            "job_id": event.EVENT_ID,
            "job": job,
            "job_args": kwargs
        })
        return event