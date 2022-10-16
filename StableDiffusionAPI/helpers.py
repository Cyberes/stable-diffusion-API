import os
from .output_parser import OutputParser
import logging
from urllib.parse import urlsplit
import json

# Various helper functions.

script_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def print_api_result(r):
    if 'status_code' in r and 'error' in r and 'response_json' in r:
        string_output = []
        if r['status_code'] != 200:
            string_output.append(f"{r['status_code']} ERROR!")
            string_output.append(f"Error Code: {r['error']}")
            string_output.append(f"Response: {r['response_json']}")
            if 'error' in r['response_json'].keys():
                string_output.append('A "None" error means that stable-diffusion-webui encountered an internal error.')
        else:
            string_output.append('200 OK!')
            string_output.append(str(r['msg'])) if r['msg'] not in [True, False, None] else ''
    else:
        return None
    return '\n'.join(string_output)


def read_response(response):
    try:
        response_json = response.json()
        parser = OutputParser(response_json['data'][1]).check_for_error()
    except Exception as e:
        logging.error(f'{response.status_code} {response.text} {getattr(e, "message", repr(e))}')
        parser = -1
        try:
            response_json = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            response_json = response.text
    return {'status_code': response.status_code,
            'msg': parser[1] if parser != -1 and not parser[0] else None,
            'error': parser[1] if parser != -1 and parser[0] else None,
            'response_json': response_json
            }


def clean_url(url):
    x = [z for z in list(urlsplit(url)) if all(z)]
    scheme = f'{x[0]}://'
    del x[0]
    return f'{scheme}{"".join(x).replace("//", "/")}'
