from opensearchpy import NotFoundError, helpers

from config import INDEX_NAME, client


def load_data():
    """Yields data from json file."""
    # full_format_recipes.json
    # https://www.kaggle.com/hugodarwood/epirecipes?select=full_format_recipes.json
    with open("full_format_recipes.json", "r") as f:
        data = json.load(f)
        for recipe in data:
            yield {"_index": INDEX_NAME, "_source": recipe}


def send_data():
    """Send multiple data to an OpenSearch client."""
    data = load_data()
    response = helpers.bulk(client, data)
    print(f"Data sent to your OpenSearch with response: {response}")


def delete_index():
    """Delete all the documents, and do not raise exceptions"""
    client.indices.delete(index=INDEX_NAME, ignore=[400, 404])


def get_document(client, doc_id, doc_name):
    """Returns OpenSearch document as a dict."""
    try:
        return client.get(index=INDEX_NAME, doc_type=doc_name, id=doc_id)
    except NotFoundError:
        print("No document found.")
