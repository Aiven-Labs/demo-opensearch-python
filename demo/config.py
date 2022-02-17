# full_format_recipes.json taken from
# https://www.kaggle.com/hugodarwood/epirecipes?select=full_format_recipes.json

import json
from logging import exception
from operator import index
import os
from opensearchpy import OpenSearch, helpers
from dotenv import load_dotenv
from typing import Dict

load_dotenv()
INDEX_NAME = "epicurious-recipes"


def load_data():
    """Yields data from json file."""
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


def search_exact(args, client=client):
    """Searching for exact matches of a value in a field."""
    field = args.param1
    value = args.param2
    query_body = {"query": {"term": {field: value}}}
    return client.search(index=INDEX_NAME, body=query_body)


def search_range(client, field, gte, lte):
    """Searching for a range of values in a field."""
    print(f"Searching for values in the {field} ranging from {gte} to {lte}")
    query_body = {"query": {"range": {field: {"gte": gte, "lte": lte}}}}
    return client.search(index=INDEX_NAME, body=query_body)


def search_fuzzy(client, field, value, fuzziness):
    """Search by specifying fuzziness to account for typos and misspelling."""
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


def search_match(client, field, query):
    """Perform search by relevance for certain field and query."""
    print(f"Searching for {query} in the field {field}")
    query_body = {"query": {"match": {field: query}}}
    return client.search(index=INDEX_NAME, body=query_body)


def search_query_string(client, field, query, size):
    """Search by using operators with query string and size parameter"""
    print(
        f"Searching for ${query} in the field ${field} and returning maximum ${size} results"
    )
    query_body = {
        "query": {
            "query_string": {
                "query": "(new york city) OR (big apple)",
                "default_field": "content",
            }
        }
    }
    return client.search(index=INDEX_NAME, body=query_body, size=size)


def search_slop(client, field, query, slop):
    """Search by specifying a slop - a distance between search word"""
    print(f"Searching for {query} with slop value {slop} in the field {field}")
    query_body = {
        "query": {"match_phrase": {field: {"query": query, "analyzer": slop}}}
    }
    return client.search(index=INDEX_NAME, body=query_body)


def search_combined_queries(client):
    query_body = {
        "query": {
            "bool": {
                "must": {"match": {"categories": "Quick & Easy"}},
                "must_not": {"match": {"ingredients": "garlic"}},
                "filter": [
                    {"range": {"protein": {"gte": 5}}},
                    {"range": {"sodium": {"lte": 50}}},
                ],
                "must_not": {"match": {"ingredients": "garlic"}},
            }
        }
    }
    return client.search(index=INDEX_NAME, body=query_body)


def send_data(client, data):
    # Send data to OpenSearch
    response = helpers.bulk(os_client, load_data())
    print(f"Data sent to your OpenSearch with response: {response}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Run search queries on OpenSearch")
    parser.add_argument("")
    FUNCTION_MAP = {"match": search_exact}
    # Connect with the cluster
    SERVICE_URI = os.getenv("SERVICE_URI")
    os_client = OpenSearch(SERVICE_URI, use_ssl=True)

    p = argparse.ArgumentParser()
    subparsers = p.add_subparsers()

    option1_parser = subparsers.add_parser("match")
    option1_parser.add_argument("param1")
    option1_parser.add_argument("param2")
    option1_parser.set_defaults(func=FUNCTION_MAP["search_exact"])

    args = p.parse_args()
    args.func(args, client=os_client)

    resp = search_match(os_client, "title", "Tomato garlic soup with dill")

    pprint.pprint(resp, width=1)


if __name__ == "__main__":
    main()
