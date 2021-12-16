"""Flask-Pub-Demo module."""
import json
import os
import time
from datetime import datetime, timezone

from simple_cloudevent import SimpleCloudEvent, to_queue_message
from flask import Flask
from flask_pub import FlaskPub

from .config import Config


publisher = FlaskPub()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    publisher.init_app(app)

    @app.route("/pub-my-event/<string:message>", methods=["POST"])
    def pub(message: str):
        '''Publish string to queue.'''

        project_id = 'sleepy-dog'
        topic = 'myFavQuote'

        ce = SimpleCloudEvent(source='com.daxiom.example.simple-ce',
                              subject='simple-ce',
                              time=datetime.utcfromtimestamp(time.time()).replace(tzinfo=timezone.utc),
                              data={'hello': message}
                            )

        subject_name = f'projects/{project_id}/topics/{topic}'

        publisher.publish(
            subject=subject_name, msg=to_queue_message(ce)
        )
        return {}, 200

    return app
