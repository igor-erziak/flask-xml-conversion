"""
Helper functions to interact with Rossum APIs (https://api.elis.rossum.ai/v1/
and https://my-little-endpoint.ok/rossum).
"""

import requests
from os import environ
from urllib.parse import urlparse
from pathlib import PurePosixPath
import base64 as b64
import sys

try:
    CREDS = {
        'username': environ['ROSSUM_USERNAME'],
        'password': environ['ROSSUM_PASSWORD']
    }
except KeyError as e:
    print(f'KeyError: the environment variable {e} is not set.')
    sys.exit('Terminating...')

ROSSUM_API = 'https://api.elis.rossum.ai/v1'
LITTLE_ENDPOINT = 'https://my-little-endpoint.ok/rossum'

def get_annotation_xml(annotation_id, auth_key):
    """Return annotation with the specified id in XML format."""
    queue_id = get_queue_id(annotation_id, auth_key)

    response = requests.get(
        f'{ROSSUM_API}/queues/{queue_id}/export',
        params={
            'status': 'exported',
            'format': 'xml',
            'id': annotation_id
        },
        headers={'Authorization': f'token {auth_key}'}
    )
    
    return response.text

def get_auth_key():
    """
    Return API authorization key as string using the credentials stored
    as env variables.
    """
    response = requests.post(
        f'{ROSSUM_API}/auth/login',
        json={
            'username': CREDS['username'],
            'password': CREDS['password']
        }
    )
    
    json_response = response.json()
    auth_key = json_response['key']
    
    return auth_key


def get_queue_id(annotation_id, auth_key):
    """Return queue id (int) where the annotation with the given id is located."""
    response = requests.get(
        f'{ROSSUM_API}/annotations/{annotation_id}',
        headers={'Authorization': f'token {auth_key}'}
    )
    
    json_response = response.json()
    queue_url = json_response['queue']
    queue_url_path = PurePosixPath(
        urlparse(
            queue_url
        ).path
    )
    queue_id = queue_url_path.parts[-1]
    
    return queue_id

def submit_xml(annotation_id, xml):
    """
    Submit base64 encoded xml data along with annotation_id to
    https://my-little-endpoint.ok/rossum and return true on success.
    """
    encoded_xml = b64.b64encode(xml)

    response = requests.post(
        LITTLE_ENDPOINT,
        json={
            'annotationId': annotation_id,
            'content': encoded_xml.decode()
        }
    )
    
    return response.ok
