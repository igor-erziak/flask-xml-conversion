"""
Helper functions to interact with Rossum APIs (https://api.elis.rossum.ai/v1/
and https://my-little-endpoint.ok/rossum).
"""

import requests
from os import environ
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath
import base64 as b64

CREDS = {
    'username': environ['ROSSUM_USERNAME'],
    'password': environ['ROSSUM_PASSWORD']
}

def get_annotation_xml(annotation_id, auth_key):
    """Return annotation with the specified id in XML format."""
    queue_id = get_queue_id(annotation_id, auth_key)

    response = requests.get(
        f'https://api.elis.rossum.ai/v1/queues/{queue_id}/export',
        params={
            'status': 'exported',
            'format': 'xml',
            'id': annotation_id
        },
        headers={'Authorization': f'token {auth_key}'}
    )
    if response:
        return response.text
    else:
        return None

def get_auth_key():
    """
    Return API authorization key as string using the credentials stored
    as env variables.
    """
    response = requests.post(
        'https://api.elis.rossum.ai/v1/auth/login',
        json={
            'username': CREDS['username'],
            'password': CREDS['password']
        }
    )
    if response:
        json_response = response.json()
        auth_key = json_response['key']
        return auth_key
    else:
        return None
    

def get_queue_id(annotation_id, auth_key):
    """Return queue id (int) where the annotation with the given id is located."""
    response = requests.get(
        f'https://elis.rossum.ai/api/v1/annotations/{annotation_id}',
        headers={'Authorization': f'token {auth_key}'}
    )
    if response:
        json_response = response.json()
        queue_url = json_response['queue']
        queue_url_path = PurePosixPath(
            unquote(
                urlparse(
                    queue_url
                ).path
            )
        )
        queue_id = int(queue_url_path.parts[-1])
        return queue_id
    else:
        return None

def submit_xml(annotation_id, xml):
    """
    Submit base64 encoded xml data along with annotation_id to
    https://my-little-endpoint.ok/rossum and return true on success.
    """

    encoded_xml = b64.b64encode(xml)

    try:
        response = requests.post(
            'https://my-little-endpoint.ok/rossum',
            json={
                'annotationId': annotation_id,
                'content': encoded_xml.decode()
            }
        )
    except Exception:
        return False

    if response:
        print(response.text)
        return True
    else:
        return False
