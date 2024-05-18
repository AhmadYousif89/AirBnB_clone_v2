#!/usr/bin/python3
"""
Script that starts a Flask web application with a route:
>>  '/states_list' that displays an HTML page with a list of all State objects
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Displays an HTML page with a list of all State objects"""
    states_dict = storage.all(State)
    state_list = [states_dict[state] for state in states_dict]
    return render_template('7-states_list.html', states=state_list)


@app.teardown_appcontext
def teardown(exception):
    """Removes the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
