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
        # full_format_recipes.json
        # https://www.kaggle.com/hugodarwood/epirecipes?select=full_format_recipes.json
        with open("full_format_recipes.json", "r") as f:
            data = json.load(f)
            for recipe in data:
                yield {"_index": INDEX_NAME, "_source": recipe}

    data = load_data()
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

    # Example:
    # dict_keys(['.kibana_1', 'epicurious-recipes'])

    for indice in indices:
        # skip the default indice `kibana` if present
        if "kibana" not in indice.lower():
            mapping_data = client.indices.get_mapping(indice)

            # Find index doc_type
            doc_type = list(mapping_data[indice]["mappings"].keys())[0]
            print("doc_type: {doc_type}")

            schema = mapping_data[indice]["mappings"][doc_type]
            print(f"Fields: {list(schema.keys())} \n")
            pprint(schema, width=80, indent=0)


def get_document():
    """Returns OpenSearch document as a dict."""
    try:
        return client.get(index=INDEX_NAME)
    except NotFoundError:
        print("No document found.")


if __name__ == "__main__":
    app()
