import re
from threading import Event
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import pandas as pd

class StockData(AsyncWebsocketConsumer):

   async def connect(self):
        self.group_name='tableData'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

   async def disconnect(self,close_code):
        pass

   async def receive(self,text_data):
        print(text_data)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type':'randomFunction',
                'value':text_data,
            }
        )

   async def randomFunction(self, event):
        # print (event['value'])
        await self.send(event['value'])



class GraphData(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name='graphData'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self,close_code):
        pass

    async def receive(self,text_data):
        print(text_data)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type':'randomFunction',
                'value':text_data,
            }
        )

    async def randomFunction(self, event):
        # print (event['value'])
        await self.send(event['value'])



class NewsData(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name='newsData'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()


    async def receive(self,text_data):
        print(text_data)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type':'randomFunction',
                'value':text_data,
            }
        )

    async def randomFunction(self, event):
        # print (event['value'])
        await self.send(event['value'])
