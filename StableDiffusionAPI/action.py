import requests
from .helpers import clean_url, read_response
import logging


class APIAction:
    def __init__(self, config, path=None):
        self.config = config
        self.path = path if path is not None else self.config.webui_base_url

    def send(self, data):
        url = clean_url(self.path)
        r = read_response(requests.post(url, json=data, timeout=self.config.timeout))
        if r['error'] == -1:
            logging.error(f'read_response() returned -1 from URL {url}')
        return r

    def send_async(self, json_data):
        """
        Send an api call then disconnect from the process.
        The user will manage polling via poll()
        """
        return

    def poll(self):
        return
