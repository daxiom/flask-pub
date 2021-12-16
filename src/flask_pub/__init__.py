import json
from typing import Final, Union

from flask import _app_ctx_stack
from flask import current_app
from google.cloud import pubsub

__version__ = '0.0.1'

EXTENSION_NAME: Final = 'FLASK_REGISTRY_PUBSUB'

def get_state(app):
    """Gets the state for the application"""
    if state := app.extensions.get(EXTENSION_NAME):
        return state
    
    raise RuntimeError('The Flask_Pub extension was not registered with the current app.')


class _QueueState:
    """Remembers configuration for the (queue, app) tuple."""

    def __init__(self, publisher):
        self.publisher = publisher
        self.connectors = {}


class FlaskPub:


    def __init__(
        self,
        app=None,
        queue_plugin=None,
        engine_options=None,
    ):
        """Initialize the queue services.
        
        If app is provided, then this is bound to that app instance.
        """
        self.app = app
        self._engine_options = engine_options or {}

        if app is not None:
            self.init_app(app)

    def init_app(
        self,
        app=None,
        queue_plugin=None,
        engine_options=None,
        ):
        """This callback can be used to initialize an application for the
        use with this queue setup.
        """
        # We intentionally don't set self.app = app, to support multiple
        # applications. If the app is passed in the constructor,
        # we set it and don't support multiple applications.

        if not (
            app.config.get('FLASK_PUB_CONFIG')
        ):
            raise RuntimeError(
                'FLASK_PUB_CONFIG needs to be set.'
            )

        app.config.setdefault('FLASK_PUB_DEFAULT_SUBJECT', None)

        self.driver = pubsub.PublisherClient()

        app.extensions[EXTENSION_NAME] = _QueueState(self)

        @app.teardown_appcontext
        def shutdown(response_or_exc):
            """Cleanup all state here as part of the Flask shutdown."""

            return response_or_exc
    
    def publish(self, msg: Union[str, bytes], subject: str = None):

        if not (app := self.app):
                app = current_app
  
        topic_name = subject or app.config.get('FLASK_PUB_DEFAULT_SUBJECT')
        
        if app and topic_name and (state := get_state(app)):

            data = msg
            if isinstance(msg, str):
                data = msg.encode("utf8")
            
            state.publisher.driver.publish(
                topic=topic_name, data=data
                )
