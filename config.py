"""
Configuration information regarding client and envs
"""
import os

from dotenv import load_dotenv
from opensearchpy import OpenSearch


load_dotenv()
INDEX_NAME = "epicurious-recipes"
SERVICE_URI = os.getenv("SERVICE_URI")
client = OpenSearch(SERVICE_URI, use_ssl=True)
