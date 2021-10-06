import os

from flask import Flask
from flask_cors import CORS
from config import config
import decimal
import flask.json

class MyJSONEncoder(flask.json.JSONEncoder):
    """customize json encoder to deal with decimal error when doing jsonify"""
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)


def create_app(test=False):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.json_encoder = MyJSONEncoder
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.mysql'),
    )

    if not test:
        # load the instance config, if it exists, when not testing
        app.config.from_object(config['development'])
    else:
        # load the test config if passed in
        app.config.from_object(config['testing'])

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .db import init_app
    init_app(app)

    from .views import clients, events, locations, suppliers, supplies, multiple_table
    app.register_blueprint(clients.mod)
    app.register_blueprint(events.mod)
    app.register_blueprint(locations.mod)
    app.register_blueprint(suppliers.mod)
    app.register_blueprint(supplies.mod)
    app.register_blueprint(multiple_table.mod)

    return app
