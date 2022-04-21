import asyncio


class Event(asyncio.Event):
    EVENT_TYPE: str
    EVENT_VALUE: dict
    EVENT_ID: str
    EVENT_TOPIC: str

    def __init__(self, event_id, event_type,  event_topic, loop):
        """
        override the python Event class
        :param event_id:
        :param event_type:
        :param event_topic:
        :param loop: loop must be passed because set and wait must be in the same loop
        """
        self.loop = loop
        super().__init__(loop=self.loop)
        self.EVENT_ID = event_id
        self.EVENT_TOPIC = event_topic
        self.EVENT_TYPE = event_type

    def trigger_event(self, value):
        """
        set the value of event when calling set
        :param value:
        :return:
        """
        self.EVENT_VALUE = value
        self.loop.call_soon_threadsafe(self.set)

    async def wait_clear(self):
        await self.wait()
        self.clear()
