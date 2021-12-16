"""Configuration for the Application."""
import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class Config:
    """Base class configuration that should set reasonable defaults.
    Used as the base for all the other configurations.
    """

    SECRET_KEY = 'a secret'

    FLASK_PUB_CONFIG={'plugins':[{'gcp': 'gcp-pub-sub'},]}
    FLASK_PUB_DEFAULT_SUBJECT='projects/unique-project-id/topics/simpleTopicName'

    TESTING = False
    DEBUG = True
