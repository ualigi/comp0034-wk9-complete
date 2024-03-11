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
- Flask app that uses the REST API: `flask --app flask_app_uses_rest run`
- Dash app that uses the REST API: `python src/dash_app_uses_rest/app_dash.py`

## Example tests

| App                         | Test examples cover                                                                                                                                                                          |
|:----------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| test_dash_with_rest         | Very basic Dash app that has content from a REST API. The REST API is run using a fixture.                                                                                                   |
| test_flask_with_rest        | Very basic Flask app that has a page from a REST API (/rest) that is accessed by clicking on a hyperlink from the home page (/). The REST API and the Flask app are both run using fixtures. |
| test_para_with_pytest_flask | tests for the Flask paralympics app that use the pytest-flask library live server fixture.                                                                                                   |
| test_iris                   | Tests for the Flask iris app. Uses fixture to run the app as a live server.                                                                                                                  |
| test_paralympics_dash       | Tests for the Dash paralympics app. Uses dash_duo fixture to run the app as a live server.                                                                                                   |
| test_paralympics_flask      | Tests for the Flask paralympics app. Uses fixture to run the app as a live server.                                                                                                           |

