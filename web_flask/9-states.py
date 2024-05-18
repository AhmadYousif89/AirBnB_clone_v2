#!/usr/bin/python3
"""
Script that starts a Flask web application with a route:
>>  '/states' that displays a list of all States
>>  '/states/<id>' that displays a list of all Cities in a State
"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Closes the current SQLAlchemy Session"""
    storage.close()


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    """Displays a list of all States"""
    if id:
        key = f"State.{id}"
        if key in storage.all("State"):
            state = storage.all("State")[key]
            return render_template('9-states.html', state=state, id=id)
    states = storage.all("State").values()
    return render_template('9-states.html', states=states)


if __name__ == '__main__':
    app.run()
