# full_format_recipes.json taken from
# https://www.kaggle.com/hugodarwood/epirecipes?select=full_format_recipes.json

import json
import os
from opensearchpy import OpenSearch
from dotenv import load_dotenv

load_dotenv()
INDEX_NAME = "epicurious-recipes"


def load_data():
    with open("full_format_recipes.json", "r") as f:
        data = json.load(f)
        for recipe in data:
            yield {"_index": INDEX_NAME, "_source": recipe}


def delete_index():
    es.indices.delete(index=INDEX_NAME, ignore=[400, 404])


def main():
    # Connect with the cluster
    SERVICE_URI = os.getenv("SERVICE_URI")
    opensearch_client = OpenSearch(SERVICE_URI, use_ssl=True)

    # Load data to OpenSearch cluster
    load_data()


if __name__ == "__main__":
    main()
