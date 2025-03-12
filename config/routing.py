from apps.clients.routing import websocket_urlpatterns as clients_websockets
from apps.planning.routing import websocket_urlpatterns as planning_websockets

websocket_urlpatterns = clients_websockets + planning_websockets