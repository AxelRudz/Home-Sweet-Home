# Home Sweet Home

[![status](https://img.shields.io/badge/Status-Beta-blue.svg)](https://github.com/AxelRudz/Home-Sweet-Home)
[![status](https://img.shields.io/badge/Official%20website-https://axelrudz.pythonanywhere.com-purple.svg)](https://axelrudz.pythonanywhere.com)

This is a simple web application that I made as an example. There are many things that I would like to add and improve in this project.

### Requirements

- python3
- virtualenv

### How to run locally (on Linux)

```bash
$ virtualenv -p python3 venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ FLASK_ENV=development
$ FLASK_APP=run.py
$ flask run
```

To quit the virtual environment you must execute:

```bash
$ deactivate
```

## Estructure of the proyect

```bash
helpers           # Module used for aux functions
models            # Model (MVC)
resources         # Controllers (MVC)
templates         # View (MVC)
db.py             # Database instance
__init__.py       # App instance and ruting
```
