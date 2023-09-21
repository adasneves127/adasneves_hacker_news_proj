"""Contains functions used for REST API calls."""

import requests


def get_data(url):
    return requests.get(url).json()
