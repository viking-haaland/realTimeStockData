from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from screener import consumer
import platform

if float(platform.python_version()[0:3]) > 3.6:
    cons = consumer.StockData.as_asgi()
    cons2 = consumer.GraphData.as_asgi()
    cons3 = consumer.NewsData.as_asgi()
    
else:
    cons = consumer.StockData
    cons2 = consumer.GraphData
    cons3 = consumer.NewsData

websocketsUrlpatterns = [
    path('ws/tableData/', cons),
    path('ws/graphData/', cons2),
    path('ws/newsData/', cons3),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(URLRouter(websocketsUrlpatterns))
})
