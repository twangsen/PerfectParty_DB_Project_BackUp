from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort, make_response
from app import db
from . import sql_helper
import psycopg2

mod = Blueprint('multiple_table', __name__)

cols = sql_helper.column_name

aggregations = ['Sum', 'Count']

@mod.route('/multi')
def index():
    return "index"

@mod.route('/multi/select', methods=['POST'])
def get_items():
    if not request.is_json:
        message = "Request is not json format"
        return make_response(jsonify(message), 400)
    args = request.get_json()
    if "from" not in args:
        message = "Request does not specify the from clause"
        return make_response(jsonify(message), 400)
    from_args = args["from"]
    for a in from_args:
        # get all tables and corresponding names
        if a is dict:
            a = sql_helper.construct_clause(a)
        if a not in cols:
            message = "Request contains invalid table name {}".format(a)
            return make_response(jsonify(message), 400)
    select_args = args["select"] if "select" in args else []
    where_args = args["where"] if "where" in args else {}
    group_args = args["group"] if "group" in args else []
    have_args = args["have"] if "have" in args else {}
    distinct = " DISTINCT" if "distinct" in args else ""
    for s in select_args:
        if 'Sum' not in s and 'Count' not in s:
            table_name, field_name = s.split('.')
            if table_name not in cols or field_name not in cols[table_name]:
                message = "Request select contains invalid field names"
                return make_response(jsonify(message), 400)
    for w in where_args:
        if 'Sum' not in w and 'Count' not in w:
            table_name, field_name = w.split('.')
            if table_name not in cols or field_name not in cols[table_name]:
                message = "Request where contains invalid field names"
                return make_response(jsonify(message), 400)
    for g in group_args:
        if 'Sum' not in g and 'Count' not in g:
            table_name, field_name = g.split('.')
            if table_name not in cols or field_name not in cols[table_name]:
                message = "Request group contains invalid field names"
                return make_response(jsonify(message), 400)
    for h in have_args:
        if 'Sum' not in h and 'Count' not in h:
            table_name, field_name = h.split('.')
            if table_name not in cols or field_name not in cols[table_name]:
                message = "Request have contains invalid field names"
                return make_response(jsonify(message), 400)
    from_clause = ",".join(from_args)
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
        cur.execute('SELECT{} {} FROM {}{}{}'.format(distinct, select_clause, from_clause, group_clause, have_clause))
    else:
        cur.execute('SELECT{} {} FROM {} WHERE {}{}{}'.format(distinct, select_clause, from_clause, where_clause, group_clause, have_clause))
    output = cur.fetchone()
    results = []
    results.append(select_args)
    while output is not None:
        results.append(output)
        output = cur.fetchone()

    # close connection
    con.commit()
    cur.close()

    return jsonify(data=results)


@mod.route('/multi/join', methods=['POST'])
def get_items_with_join():
    if not request.is_json:
        message = "Request is not json format"
        return make_response(jsonify(message), 400)
    args = request.get_json()
    if "from" not in args:
        message = "Request does not specify the from clause"
        return make_response(jsonify(message), 400)
    from_args = args["from"]
    if type(from_args) != dict:
        for a in from_args:
            if a not in cols:
                message = "Request contains invalid table name {}".format(a)
                return make_response(jsonify(message), 400)
    select_args = args["select"] if "select" in args else []
    where_args = args["where"] if "where" in args else {}
    group_args = args["group"] if "group" in args else []
    have_args = args["have"] if "have" in args else {}
    join_args = " " + args["join"] + " " if "join" in args else None
    on_args = args["on"] if "on" in args else {}
    distinct = " DISTINCT" if "distinct" in args else ""
    if join_args is None:
        join_args = " AND "
    for s in select_args:
        if "Sum" not in s and "Count" not in s:
            table_name, field_name = s.split('.')
            if table_name not in cols or field_name not in cols[table_name]:
                message = "Request select contains invalid field names"
                return make_response(jsonify(message), 400)
    for w in where_args:
        if "Sum" not in w and "Count" not in w:
            if '.' in w:
                table_name, field_name = w.split('.')
                if table_name not in cols or field_name not in cols[table_name]:
                    message = "Request where contains invalid field names"
                    return make_response(jsonify(message), 400)
    for g in group_args:
        if 'Sum' not in g and 'Count' not in g:
            table_name, field_name = g.split('.')
            if table_name not in cols or field_name not in cols[table_name]:
                message = "Request group contains invalid field names"
                return make_response(jsonify(message), 400)
    for h in have_args:
        if 'Sum' not in h and 'Count' not in h:
            table_name, field_name = h.split('.')
            if table_name not in cols or field_name not in cols[table_name]:
                message = "Request have contains invalid field names"
                return make_response(jsonify(message), 400)
    on_clause = ""
    if on_args != {}:
        on_clause = " ON {}".format(sql_helper.construct_clause(on_args))
    if type(from_args) == dict:
        from_clause = "(SELECT {} FROM {} ON {}) AS FOO".format(','.join(from_args["select"]),
                                                                  from_args["join"].join(from_args["from"]),
                                                                  sql_helper.construct_clause(from_args["on"]))
    else:
        from_clause = "({}{})".format(join_args.join(from_args), on_clause)
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
        cur.execute('SELECT{} {} FROM {}{}{}'.format(distinct, select_clause, from_clause, group_clause, have_clause))
    else:
        cur.execute('SELECT{} {} FROM {} WHERE {}{}{}'.format(distinct, select_clause, from_clause, where_clause, group_clause, have_clause))
    print('SELECT{} {} FROM {} WHERE {}{}{}'.format(distinct, select_clause, from_clause, where_clause, group_clause, have_clause))
    output = cur.fetchone()
    results = []
    results.append(select_args)
    while output is not None:
        results.append(output)
        output = cur.fetchone()

    # close connection
    con.commit()
    cur.close()

    return jsonify(data=results)


@mod.route('/multi/command', methods=['POST'])
def command():
    if not request.is_json:
        message = "Request is not json format"
        return make_response(jsonify(message), 400)
    args = request.get_json()
    if "command" not in args or args["command"] is not str:
        message = "Request does not contains a valid command"
        return make_response(jsonify(message), 400)
    c = args["command"]
    if "{}" not in c:
        # connect to DB
        con = db.get_connection()
        cur = con.cursor()
        cur.execute(c)
        output = cur.fetchone()
        results = []
        while output is not None:
            results.append(output)
            output = cur.fetchone()
        # close connection
        con.commit()
        cur.close()
    else:
        number_unkown = c.count("{}")
        if "value" not in args or args["value"] is not list:
            message = "Request does not provides a valid value list"
            return make_response(jsonify(message), 400)
        value_args = args["value"]
        if number_unkown != len(value_args):
            message = "Request does not provides a valid value list"
            return make_response(jsonify(message), 400)
        # connect to DB
        con = db.get_connection()
        cur = con.cursor()
        cur.execute(c.format(*value_args))
        output = cur.fetchone()
        results = []
        while output is not None:
            results.append(output)
            output = cur.fetchone()
        # close connection
        con.commit()
        cur.close()

    return jsonify(data=results)
