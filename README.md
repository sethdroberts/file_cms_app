# File CMS App
Designed for PY175

## Steps to set up:

Install pipx
```python
pip install pipx
```

Install poetry using pipx:
```python
pipx install poetry
```

Create new poetry project:
```python
poetry new file_cms_app
```

Add flask as dependency:
```python
poetry add flask
```

Lock and install all dependencies:
```python
poetry lock
poetry install
```

Add ```app.py``` file with basic Flask routing to '/' (change port to ```5003```if not in Cloud9)
```python
from flask import Flask
app = Flask(__name__)


@app.route("/")
def index():
    return "Getting started"
    
if __name__ == "__main__":
    app.run(debug=True, port=8080)
```

Run locally:
```python
poetry run python app.py
```

Commit to Github!

Run tests using ```unittest```:
```python
poetry run python -m unittest tests.test_app
```

NOTE- When sending to Render:
1. Make sure to use the old version of the toml file (not the auto-generated one - still can't get it it to work). You can manually add in dependencies to start, and the use ```poetry lock``` to upgrade.
2. 2. Make sure you have a folder with ```__init__.py``` inside in the root directory with same name as project file in the toml file. Seems necessary to avoid tricky errors from ```poetry install```.