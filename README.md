##

* Fork, clone, checkout development, checkout -b topic, push, PR - link to docs when created -



## Setup Jupyter-book

### Steps I took for Ubuntu 18

* Setup and start a virtual environment to keep everything tidy.
<code>apt install python3-venv</code>
<code>python3 -m venv .cistemdocs</code>
<code>source .cistemdocs/bin/activate</code>
* You may not need to uninstall wheel. I had some funny error.
<code>pip uninstall wheel</code>
<code>pip install wheel</code>
<code>pip install contextvars</code>
<code>pip install -U jupyter-book</code>
<code>pip install numpy</code>
<code>pip install matplotlib</code>

### To build (--all arg is optional, but it seems like some changes are not observered leading to no new build?)
<code>jupyter-book build --all cisTEM_docs && firefox cisTEM_docs/_build/html/index.html</code>
