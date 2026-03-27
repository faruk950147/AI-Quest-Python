from django.urls import path
from office.consumers import OfficeAsyncConsumer

websocket_urlpatterns = [
    path('ws/office/', OfficeAsyncConsumer.as_asgi()),
]
# ws://127.0.0.1:8000/ws/office/