OpenSearch® search queries with Python
======================================

This repository contains code examples related to <Add devportal page>.

Quickstart
-----------

To run those examples you need:

* An OpenSearch® cluster. It can be `set it up manually <https://opensearch.org/downloads.html>`_ or you can use a fully managed service, such as `Aiven for OpenSearch® <https://aiven.io/opensearch>`_.
* `Python 3.7+ <https://www.python.org/downloads/>`_.

Install all dependencies::

    pip install -r requirements.txt


Repository structure
--------------------

* ``index.py`` - load data to cluster functions

* ``search.py`` - search queries examples

* ``config.py`` - connection operation to the cluster

* ``helpers.js`` - response handler of search requests


Search examples
---------------
The available search options can be found by using help command::

    python search.py --help

Find the arguments to be passed to a certain function by running::

    python search.py OPTION --help


OPTION can be:
* match
* multi-match
* match-phrase
* fuzzy
* term 
* slop
* range
* query-string
* slop
* combine

Do you have questions?
----------------------
Feel free to open an issue with your question on `Issues` or drop me a message at laysa.uchoa@aiven.com


License
-------

This work is licensed under the Apache License, Version 2.0. Full license text is available in the LICENSE file and at http://www.apache.org/licenses/LICENSE-2.0.txt


Trademarks
----------

OpenSearch, Python are trademarks and property of their respective owners. All product and service names used in this website are for identification purposes only and do not imply endorsement.
