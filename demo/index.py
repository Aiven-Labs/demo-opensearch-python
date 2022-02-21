"""
Functions related to index operations:
send data to cluster, delete index, 
get cluster info and get mapping
"""
import json
from pprint import pprint

import typer
from opensearchpy import NotFoundError, helpers, OpenSearch

from config import INDEX_NAME, client


app = typer.Typer()


@app.command("send-data")
def send_data():
    """Send multiple data to an OpenSearch client."""

    def load_data():
        """Yields data from json file."""
        # full_format_recipes.json source:
        # https://www.kaggle.com/hugodarwood/epirecipes?select=full_format_recipes.json
        with open("full_format_recipes.json", "r") as f:
            data = json.load(f)
            for recipe in data:
                yield {"_index": INDEX_NAME, "_source": recipe}

    data = load_data()
    print(f"Ingesting {INDEX_NAME} data")
    response = helpers.bulk(client, data)
    print(f"Data sent to your OpenSearch with response: {response}")


@app.command("delete-index")
def delete_index(index_name=INDEX_NAME):
    """Delete all the documents of certain index name, and do not raise exceptions"""
    client.indices.delete(index=index_name, ignore=[400, 404])


@app.command("get-cluster-info")
def get_cluster_info():
    """Get information about your OpenSearch cluster"""
    return pprint(OpenSearch.info(client), width=100, indent=1)


@app.command("get-mapping")
def get_mapping():
    """Retrieve mapping for the index.
    The mapping lists all the fields and their data types."""

    # list of all the cluster's indices
    indices = client.indices.get_alias("*").keys()
    print(f"All indices: {indices}")

    # Example:
    # dict_keys(['.kibana_1', 'epicurious-recipes'])

    mapping_data = client.indices.get_mapping(INDEX_NAME)

    # Find index doc_type
    doc_type = list(mapping_data[INDEX_NAME]["mappings"].keys())[0]
    print("doc_type: {doc_type}")

    schema = mapping_data[INDEX_NAME]["mappings"][doc_type]
    print(f"Fields: {list(schema.keys())} \n")
    pprint(schema, width=80, indent=0)


if __name__ == "__main__":
    app()
