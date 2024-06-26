import json
import asyncio
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
from django.template.loader import render_to_string

from .models import Portfolio


class UserTickerConsumer(WebsocketConsumer):

    def connect(self):
        self.portfolio_id = self.scope["url_route"]["kwargs"]["port_id"]
        self.portfolio_group_name = f"Portfolio:{self.portfolio_id}"
        async_to_sync(self.channel_layer.group_add)(
            self.portfolio_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        pass



class TickerConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["port_id"]
        self.room_group_name = f"portfolio_{self.room_name}"


        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        

    @sync_to_async
    def fetch_data_from_db(self):
        instance = get_object_or_404(Portfolio, id=self.room_name)
        return instance

    async def fetch_html_message(self):
        instance = await self.fetch_data_from_db()
        instance_dict = model_to_dict(instance)
        serialized_instance = json.dumps(instance_dict)
        context = {'instance': instance}  # Add any context variables needed for rendering
        html_message = await render_to_string('ajax/tickers_container.html', context)
        print('html_message', html_message)
        return html_message

    async def disconnect(self, code):
       await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        data = self.fetch_html_message()

        instance = await self.fetch_data_from_db()
        instance_dict = model_to_dict(instance)
        serialized_instance = json.dumps(instance_dict, indent=4, sort_keys=True, default=str)

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "refresh.message", "message": serialized_instance}
        )

    async def refresh_message(self, event):
        message = event['message']
        await self.send(
            text_data=json.dumps({
                'message': message,
               
            })
        )

  
