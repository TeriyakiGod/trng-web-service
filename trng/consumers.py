import collections
from ctypes import c_uint32
import struct
from channels.generic.websocket import WebsocketConsumer
import requests
from . import logger
from .models import Generator

class TrngConsumer(WebsocketConsumer):    
    buffer: collections.deque[c_uint32] = collections.deque(maxlen=1000000000)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def connect(self):
        self.ip = self.scope['client'][0]  
        gen = Generator.objects.get_or_create(ip=self.ip)[0]
        gen.online = True
        api_response = requests.get(f"http://ip-api.com/json/{self.ip}").json()
        gen.country = api_response.get("country", "Unknown")
        gen.city = api_response.get("city", "Unknown")
        gen.save()
        self.accept()

    def disconnect(self, close_code):
        Generator.objects.filter(ip=self.ip).update(online=False)

    def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            # Convert bytes to unsigned int
            random_number: c_uint32 = struct.unpack('<I', bytes_data)[0]
            # Add the random number to the buffer
            self.buffer.appendleft(random_number)
        elif text_data:
            logger.info(f"Received text data: {text_data}")
            pass
        else:
            logger.info("Received unidentified data")
            pass