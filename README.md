# demo-opensearch-python
How to set up Elasticsearch with an Aiven account and send pandas dataframe to your Elasticsearch endpoint.

# Quickstart


Install all dependencies:

``` shell
$ pip install -r requirements.txt
```

Have an Elasticsearch running on the cloud or in your local machine with a valid endpoint.

```shell
python pandas_to_es.py --url <https://<user>:<password>@<host>:<port>
```

If you are looking for a cloud service provider to run your Elasticsearch service, check out [Aiven for Elasticsearch](https://help.aiven.io/en/articles/489571-getting-started-with-aiven-for-elasticsearch).

**Note:** check `blog/pandas_to_es.md` to dive into the code details.
# License
Apart from the content on the `blog/`, everything else is licensed under MIT.
# Questions

**Do you have questions?**
Feel free to open an issue with your question on `Issues` or drop me a message at laysa.uchoa@gmail.com
