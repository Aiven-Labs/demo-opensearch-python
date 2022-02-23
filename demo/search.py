"""
This file contains code samples for search queries.
Run the following to check the available methods:

.. code-block:: shellpython

   python search.py --help

"""
import pprint
from operator import imod

import typer

from config import INDEX_NAME, SERVICE_URI, client


app = typer.Typer()


@app.command("range")
def search_range(field, gte, lte):
    typer.echo(f"Searching for values in the {field} ranging from {gte} to {lte}")
    query_body = {"query": {"range": {field: {"gte": gte, "lte": lte}}}}
    return query_body


@app.command("fuzzy")
def search_fuzzy(field, value, fuzziness):
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
    resp = client.search(index=INDEX_NAME, body=query_body)
    pprint.pprint(resp, width=100, indent=1)


@app.command("match")
def search_match(field, query):
    """Perform search by relevance for certain field and query."""
    print(f"Searching for {query} in the field {field}\n")
    query_body = {"query": {"match": {field: query}}}
    resp = client.search(index=INDEX_NAME, body=query_body)
    pprint.pprint(resp, width=100, indent=1)


@app.command("query-string")
def search_query_string(field, query, size):
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
    resp = client.search(index=INDEX_NAME, body=query_body)
    typer.echo(pprint.pprint(resp, width=100, indent=1))


@app.command("slop")
def search_slop(field, query, slop):
    """Search by specifying a slop - a distance between search word"""
    print(f"Searching for {query} with slop value {slop} in the field {field}")
    query_body = {
        "query": {"match_phrase": {field: {"query": query, "analyzer": slop}}}
    }
    resp = client.search(index=INDEX_NAME, body=query_body)
    typer.echo(pprint.pprint(resp, width=100, indent=1))


@app.command("combine")
def search_combined_queries():
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
    resp = client.search(index=INDEX_NAME, body=query_body)
    typer.echo(pprint.pprint(resp, width=100, indent=1))


@app.command("term")
def search_exact(field: str, value: int):
    """Searching for exact matches of a value in a field."""
    query_body = {"query": {"term": {field: value}}}
    resp = client.search(index=INDEX_NAME, body=query_body)
    typer.echo(pprint.pprint(resp, width=100, indent=1))


if __name__ == "__main__":
    app()
