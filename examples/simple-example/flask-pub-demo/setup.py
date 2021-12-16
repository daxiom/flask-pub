"""Installer and setup for this module
"""
import ast
from glob import glob
from os.path import basename, splitext
import re

from setuptools import setup, find_packages


def read_requirements(filename):
    """
    Get application requirements from
    the requirements.txt file.
    :return: Python requirements
    """
    with open(filename, 'r') as req:
        requirements = req.readlines()
    install_requires = [r.strip() for r in requirements if r.find('git+') != 0]
    return install_requires


def read(filepath):
    """
    Read the contents from a file.
    :param str filepath: path to the file to be read
    :return: file contents
    """
    with open(filepath, 'r') as file_handle:
        content = file_handle.read()
    return content


REQUIREMENTS = read_requirements('requirements.txt')

setup(
    name="Flask-Pub-Demo",
    install_requires=REQUIREMENTS,
)
