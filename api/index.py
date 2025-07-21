from fastapi import FastAPI
import sys
import os

# Ensure src is in the path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.service.api import app as fastapi_app

app = fastapi_app 