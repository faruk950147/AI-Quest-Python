from django.urls import path
from office.consumers import OfficeSyncConsumer, OfficeAsyncConsumer

websocket_urlpatterns = [
    path('ws/office/', OfficeSyncConsumer.as_asgi()),
    path('ws/office-async/', OfficeAsyncConsumer.as_asgi()),
]
# ws://127.0.0.1:8000/ws/office/
# ws://127.0.0.1:8000/ws/office-async/