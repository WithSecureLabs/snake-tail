
import os

if 'SNAKE_URL' in os.environ.keys():
    SNAKE_URL = os.environ["SNAKE_URL"]

else:
    SNAKE_URL = 'http://localhost:5000'
