# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer
# from channels.layers import get_channel_layer
#
#
#
#
#
#
# class Notifications(WebsocketConsumer):
#     def connect(self, **kwargs):
#         self.accept()
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)("admin", {"type": "User", "message": "Date is going to expired"})
#
#     # def disconnect(self, close_code):
#     #     channel_layer = get_channel_layer()
#     #     async_to_sync(channel_layer.group_send)("admin", {"type": "User", "message": "minus"})


from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("notify", self.channel_name)
        print(f"Added {self.channel_name} channel to notification")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notify", self.channel_name)
        print(f"Removed {self.channel_name} channel to notification")

    async def user_notify(self, event):
        self.user = self.scope["user"]
        print("user is ",self.user)
        await self.send_json(event)
        print(f"Got message {event} at {self.channel_name}")





