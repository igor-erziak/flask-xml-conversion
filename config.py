from os import environ
import sys

try:
    ROSSUM_USERNAME = environ['ROSSUM_USERNAME']
    ROSSUM_PASSWORD = environ['ROSSUM_PASSWORD']
    APP_USERNAME = environ["APP_USERNAME"]
    APP_PASSWORD = environ["APP_PASSWORD"]
except KeyError as e:
    print(f'KeyError: the environment variable {e} is not set.')
    sys.exit('Terminating...')