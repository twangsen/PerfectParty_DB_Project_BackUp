
# keep track of column names
column_name = {
    "client": ["ClientID", "ClientFirstName", "ClientLastName", "ClientPassword", "ClientEmail"],
    "event": ["EventID", "ClientID", "LocationID", "Budget",  "StartDate", "EndDate", "EventType", "Organizer"],
    "location": ["LocationID", "StreetAddress", "ApartmentNumber",
                 "City", "State", "ZipCode", "Capacity", "LocationType"],
    "supplier": ["SupplierID", "Price", "SupplierType"],
    "catering": ["SupplierID", "CateringName", "CateringType"],
    "decor": ["SupplierID", "DecorName", "DecorType"],
    "entertain": ["SupplierID", "EntertainName", "EntertainType"],
    "supply": ["SupplierID", "EventID", "Amount"]
}

eachProduct = {
    'where': {
        'eventID': '\'000001\'',
        'locationID': {
            'select': []

        }
    }
}

def construct_clause(args, connector="AND"):
    """take a dict of args returns a string with the form col_name=value [connector] col_name<value etc"""
    first = True
    clause = ""
    for w in args:
        if first:
            if w is dict:
                where_clause = construct_clause(args[w]["where"]) if "where" in args[w] else ""
                if where_clause != "":
                    clause += "{} in (SELECT {} FROM {} WHERE {})".format(w, w, w["from"], where_clause)
                else:
                    clause += "{} in (SELECT {} FROM {})".format(w, w, w["from"])
            else:
                clause += "{}{}".format(w, args[w])
            first = False
        else:
            if w is dict:
                where_clause = construct_clause(args[w]["where"]) if "where" in args[w] else ""
                if where_clause != "":
                    clause += " {} {} in (SELECT {} FROM {} WHERE {})".format(connector, w, w, w["from"], where_clause)
                else:
                    clause += " {} {} in (SELECT {} FROM {})".format(connector, w, w, w["from"])
            else:
                clause += " {} {}{}".format(connector, w, args[w])
    return clause
