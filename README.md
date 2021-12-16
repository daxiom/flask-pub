# flask-pub


A simple library as a flask extension to publish messages on supported queues.

Follows common flask patterns.

```python
# config.py
class Config:
    """Base class configuration that should set reasonable defaults.
    Used as the base for all the other configurations.
    """

    FLASK_PUB_CONFIG={'plugins':[{'gcp': 'gcp-pub-sub'},]}
    FLASK_PUB_DEFAULT_SUBJECT='projects/project-id/topics/my-topic'
```


```python
# __init__.py

from flask import Flask, request
from flask_pub import FlaskPub

from .config import Config


publisher = FlaskPub()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    publisher.init_app(app)

    @app.route("/pub-my-event/<string:message>", methods=["POST"])
    def pub(message: str):
        """Publish a string to the queue."""

        non_default_subject = 'projects/my-project-id/topics/myTestTopic'

        publisher.publish(subject=topic_name, msg=message)

        return {}, 200

    return app
```
