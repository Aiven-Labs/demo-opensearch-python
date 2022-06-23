"""
Configuration information regarding client and envs
"""
import os

from dotenv import load_dotenv
from opensearchpy import OpenSearch
from customized_exceptions import InvalidServiceURI


INDEX_NAME = "recipes"


def create_client():
    """Create OpenSearch client."""
    load_dotenv()
    SERVICE_URI = os.getenv("SERVICE_URI")
    if SERVICE_URI == "https://user:pass@hostname:port" or SERVICE_URI is None:
        raise InvalidServiceURI(
            f"Update SERVICE_URI to your cluster uri. Current value for SERVICE_URI={SERVICE_URI}"
        )
    return OpenSearch(SERVICE_URI, use_ssl=True)
