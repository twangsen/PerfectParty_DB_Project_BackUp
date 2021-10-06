from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort, make_response
from app import db
from . import sql_helper
import psycopg2

mod = Blueprint('locations', __name__)

col = sql_helper.column_name["location"]

@mod.route('/location')
def index():
    return "index"

@mod.route('/location/select', methods=['GET', 'POST'])
def get_location():
    if request.method == 'POST':
        if not request.is_json:
            message = "Request is not json format"
            return make_response(jsonify(message), 400)
        args = request.get_json()
        select_args = args["select"] if "select" in args else []
        where_args = args["where"] if "where" in args else {}
        group_args = args["group"] if "group" in args else []
        have_args = args["have"] if "have" in args else {}
        if (not all(key in col for key in where_args.keys())) or (not all(key in col for key in select_args)):
            for key in where_args.keys():
                print(key in col)
            message = "Request contains invalid field names"
            return make_response(jsonify(message), 400)
        if (not all(key in col for key in have_args.keys())) or (not all(key in col for key in group_args)):
            message = "Request contains invalid field names"
            return make_response(jsonify(message), 400)
        where_clause = sql_helper.construct_clause(where_args)
        if not list(select_args):
            select_clause = "*"
        else:
            select_clause = "(" + ",".join(select_args) + ")"
        group_clause = ""
        if len(group_args) > 0:
            group_clause = " GROUP BY (" + ",".join(group_args) + ")"
        have_clause = ""
        if group_clause and len(have_args) > 0:
            have_clause = " HAVING {}".format(sql_helper.construct_clause(have_args))
        # connect to DB
        con = db.get_connection()
        cur = con.cursor()
        if not where_args:
            cur.execute('SELECT {} FROM location{}{}'.format(select_clause, group_clause, have_clause))
        else:
            cur.execute('SELECT {} FROM location WHERE {}{}{}'.format(select_clause, where_clause, group_clause, have_clause))
        output = cur.fetchone()
        results = []
        results.append(select_args)
        while output is not None:
            results.append(output)
            output = cur.fetchone()
    else:
        # connect to DB
        con = db.get_connection()
        cur = con.cursor()
        # get all
        cur.execute('SELECT * FROM location')
        output = cur.fetchone()
        results = []
        while output is not None:
            results.append(output)
            output = cur.fetchone()

    # close connection
    con.commit()
    cur.close()

    return jsonify(data=results)


@mod.route('/location/update', methods=['PUT'])
def update_location():
    if not request.is_json:
        message = "Request is not json format"
        return make_response(jsonify(message), 400)
    args = request.get_json()
    set_args = args["set"] if "set" in args else {}
    where_args = args["where"] if "where" in args else {}
    if not all(key in col for key in set_args.keys()) or not all(key in col for key in where_args.keys()):
        message = "Request contains invalid field names"
        return make_response(jsonify(message), 400)
    where_clause = sql_helper.construct_clause(where_args)
    set_clause = sql_helper.construct_clause(set_args, ",")
    # connect to DB
    con = db.get_connection()
    cur = con.cursor()
    try:
        cur.execute('Update location SET {} WHERE {}'.format(set_clause, where_clause))
        message = "Update correct with {} rows affected".format(cur.rowcount)
        code = 200
    except psycopg2.Error as e:
        message = "Update failed with error {}".format(e)
        code = 400

    # close connection
    con.commit()
    cur.close()

    return make_response(jsonify(message), code)



@mod.route('/location/insert', methods=['PUT'])
def insert_location():
    if not request.is_json:
        message = "Request is not json format"
        return make_response(jsonify(message), 400)
    args = request.get_json()
    into_args = args["into"] if "into" in args else []
    values_args = args["values"] if "values" in args else []
    if not all(key in col for key in into_args):
        message = "Request contains invalid field names"
        return make_response(jsonify(message), 400)
    into_clause = "(" + ",".join(into_args) + ")"
    values_clause = "(" + ",".join(values_args) + ")"
    # connect to DB
    con = db.get_connection()
    cur = con.cursor()
    try:
        cur.execute('INSERT INTO location {} Values {}'.format(into_clause, values_clause))
        message = "Insert correct with {} rows affected".format(cur.rowcount)
        code = 200
    except psycopg2.Error as e:
        message = "Insert failed with error {}".format(e)
        code = 400

    # close connection
    con.commit()
    cur.close()

    return make_response(jsonify(message), code)

@mod.route('/location/delete', methods=['DELETE'])
def delete_location():
    if not request.is_json:
        message = "Request is not json format"
        return make_response(jsonify(message), 400)
    args = request.get_json()
    where_args = args["where"] if "where" in args else {}
    if not all(key in col for key in where_args.keys()):
        message = "Request contains invalid field names"
        return make_response(jsonify(message), 400)
    where_clause = sql_helper.construct_clause(where_args)
    # connect to DB
    con = db.get_connection()
    cur = con.cursor()
    try:
        cur.execute('Delete from location WHERE {}'.format(where_clause))
        message = "Delete correct with {} rows affected".format(cur.rowcount)
        code = 200
    except psycopg2.Error as e:
        message = "Delete failed with error {}".format(e)
        code = 400

    # close connection
    con.commit()
    cur.close()

    return make_response(jsonify(message), code)

@mod.route('/location/id', methods=['GET'])
def get_nextid():
    # connect to DB
    con = db.get_connection()
    cur = con.cursor()
    cur.execute('Select last_value + 1 FROM location_locationid_seq')
    output = cur.fetchone()

    # close connection
    con.commit()
    cur.close()

    return jsonify(data=output)
