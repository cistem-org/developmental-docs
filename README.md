#

# Adding to the docs

## How-To work

### gitflow

* Fork, clone, checkout development, checkout -b topic, push, PR - link to docs when created -

### Setup Jupyter-book

#### Steps I took for Ubuntu 18

Setup and start a virtual environment to keep everything tidy.
<code>apt install python3-venv</code>

You could use conda or whatever you want here.
<code>python3 -m venv .cistemdocs</code>
Activate the environment (will depend on your env software obviously)
<code>source .cistemdocs/bin/activate</code>

You may not need to uninstall wheel. I had some funny error.
<code>pip uninstall wheel</code>

Install remaining dependencies
<code>pip install wheel contextvars numpy matplotlib</code>

Finally install jupyter-book
<code>pip install -U jupyter-book</code>

#### To build (--all arg is optional, but it seems like some changes are not observered leading to no new build?)
<code>jupyter-book build --all cisTEM_docs && firefox cisTEM_docs/_build/html/index.html</code>
