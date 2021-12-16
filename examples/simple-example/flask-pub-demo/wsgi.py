"""Provides the WSGI entry point for running the application
"""
import os

from flask_pub_demo import create_app


application = create_app() # pylint: disable=invalid-name

if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080
    application.run(host="127.0.0.1", port=PORT, debug=False)
