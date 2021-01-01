# mysite/asgi.py
import os
import django
django.setup()
from django.conf import settings
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.staticfiles import StaticFilesConsumer
from channels.staticfiles import StaticFilesWrapper
from asgi_middleware_static_file import ASGIMiddlewareStaticFile
from django.core.asgi import get_asgi_application
import home.routing
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todo.settings")
# os.environ['DJANGO_SETTINGS_MODULE'] = 'todo.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')

app = get_asgi_application()
app = ASGIMiddlewareStaticFile(
    app, static_url=settings.STATIC_URL, static_paths=[settings.STATIC_ROOT]
)

application = ProtocolTypeRouter({
    "http": app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            home.routing.websocket_urlpatterns
        ),
    ),
})


