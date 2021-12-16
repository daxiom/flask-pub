"""Flask-Pub-Demo module."""
import json
import os

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

        subject_name = f'projects/{project_id}/topics/{topic}'

        publisher.publish(
            subject=subject_name, msg=message
        )
        return {}, 200

    return app
