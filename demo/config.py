# full_format_recipes.json taken from
# https://www.kaggle.com/hugodarwood/epirecipes?select=full_format_recipes.json

import json
from logging import exception
import os
from opensearchpy import OpenSearch, helpers
from dotenv import load_dotenv
from typing import Dict

load_dotenv()
INDEX_NAME = "epicurious-recipes"


def load_data():
    """Yields the data to be sent to cluster."""
    with open("full_format_recipes.json", "r") as f:
        data = json.load(f)
        for recipe in data:
            yield {"_index": INDEX_NAME, "_source": recipe}


def delete_index():
    """Delete all the documents"""
    OS_CLIENT.indices.delete(index=INDEX_NAME, ignore=[400, 404])


def get_document(client, doc_id, doc_name):
    """Returns OpenSearch document as a dict."""
    try:
        return client.get(index=INDEX_NAME, doc_type=doc_name, id=doc_id)
    except NotFoundError:
        print("No document found.")


def search_exact(client, field, value):
    """Searching for exact matches of a value in a field."""
    query_body = {"query": {"term": {field: value}}}
    return client.search(index=INDEX_NAME, body=query_body)


def search_range(client, field, gte, lte):
    """Searching for a range of values in a field."""
    print(f"Searching for values in the {field} ranging from {gte} to {lte}")
    query_body = {"query": {"range": {field: {"gte": gte, "lte": lte}}}}
    return client.search(index=INDEX_NAME, body=query_body)


def search_fuzzy(field, value, fuzziness):
    """Specifying fuzziness to account for typos and misspelling."""
    print(f"Search for {value} in the {field} with fuzziness set to {fuzziness}")
    query_body = {
        "query": {
            "fuzzy": {
                field: {
                    "value": value,
                    "fuzziness": fuzziness,
                }
            }
        }
    }
    return client.search(index=INDEX_NAME, body=query_body)


def search_match(field, query):
    """Finding matches sorted by relevance."""
    print(f"Searching for {query} in the field {field}")
    query_body = {"query": {"match": {field: query}}}
    return client.search(index=INDEX_NAME, body=query_body)


def search_slop(client, field, query, slop):
    """Specifying a slop - a distance between search word"""
    print(f"Searching for {query} with slop value {slop} in the field {field}")
    query_body = {
        "query": {"match_phrase": {field: {"query": query, "analyzer": slop}}}
    }
    return client.search(index=INDEX_NAME, body=query_body)


def main():
    # Connect with the cluster
    SERVICE_URI = os.getenv("SERVICE_URI")
    OS_CLIENT = OpenSearch(SERVICE_URI, use_ssl=True)

    # Send data to OpenSearch
    try:
        response = helpers.bulk(OS_CLIENT, load_data())
        print(f"Data sent to your OpenSearch with response: {response}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
