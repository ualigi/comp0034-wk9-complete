# COMP0034 Completed example of the week 9 activities

## Set-up

1. Fork the repository
2. Clone the forked repository to create a project in your IDE
3. Create and activate a virtual environment in the project folder e.g.

    - MacOS: `python3 -m venv .venv` then `source .venv/bin/activate`
    - Windows: `py -m venv .venv` then `.venv\Scripts\activate`
4. Check `pip` is the latest versions: `pip install --upgrade pip`
5. Install the requirements. You may wish to edit [requirements.txt](requirements.txt) first to remove the packages for
   Flask or Dash if you only want to complete the activities for one type of app.

    - e.g. `pip install -r requirements.txt`
6. Install the paralympics app code e.g. `pip install -e .`

## Running the apps in the src directory

This repository contains 4 apps used in the activities which may cause some confusion for imports.

Remember to run `pip install -e .`

The 4 apps can be run from the terminal as follows, you may need to use 'py' or 'python3' instead of 'python' depending
on your operating system and python version:

- Dash app: `python src/paralympics_dash/paralympics_dash.py`
- Flask REST API app (coursework 1): `flask --app paralympics_rest run`
- Flask app: `flask --app paralympics_flask run`
- Flask ML app (Iris prediction): `flask --app "flask_iris:create_app('test')" run`