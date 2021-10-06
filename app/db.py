import mysql.connector
import psycopg2

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_connection():
    if 'con' not in g:
        con = psycopg2.connect(
            database=current_app.config["DB_NAME"],
            user=current_app.config["DB_USER"],
            host=current_app.config["DB_HOST"],
            port=current_app.config["DB_PORT"])
        con.autocommit = True
        g.con = con

    return g.con


def init_db():
    with current_app.app_context():
        con = get_connection()
        con.autocommit = True
        cur = con.cursor()

        with current_app.open_resource('schema.sql') as f:
            cur.execute(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def close_db(e=None):
    con = g.pop('con', None)

    if con is not None:
        con.close()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
