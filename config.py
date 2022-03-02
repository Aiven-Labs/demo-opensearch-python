"""
Configuration information regarding client and envs
"""
import os

from dotenv import load_dotenv
from opensearchpy import OpenSearch
from exceptions import Misconfiguration

load_dotenv()
INDEX_NAME = "epicurious-recipes"
SERVICE_URI = os.getenv("SERVICE_URI")

if SERVICE_URI == "https://user:pass@hostname:port":
    raise Misconfiguration("Update `SERVICE_URI` on .env with your cluster URI")

client = OpenSearch(SERVICE_URI, use_ssl=True)
