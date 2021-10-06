# CS348 Web Application API
CS348 web application's backend, using Postgresql, python and flask.

## Environment setup
Note: For mac & linux only.

Create a new virtual environment and activate it, then:
```
pip install -r requirements.txt
```

## DB Setup
The application uses postgres as the underlying DB.

- Install and setup postgres (if not done before):
    ```shell
    brew install postgresql # for mac
    sudo apt-get install postgresql # for linux
    ```
    ```shell
    initdb /usr/local/var/postgres
    pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start # start postgres
    # create user and db
    createdb
    psql
    ```
    Then in psql shell:
    ```sql
    -- set user's password to whatever you want, and change DB_PASSWORD value in config.py to your password
    CREATE USER postgres WITH PASSWORD 'password';
    DROP DATABASE postgres;
    CREATE DATABASE postgres OWNER postgres;
    GRANT ALL PRIVILEGES ON DATABASE postgres to postgres;
    ALTER ROLE postgres CREATEDB;
    ```

- After setup postgres, import data:
    ```shell
    # in project root directory
    psql -U postgres -f app/schema.sql
    ```

## Startup the API
- For Linux and Mac:
    ```shell
    export FLASK_APP=app
    export FLASK_ENV=development
    flask run
    ```

- For Windows cmd, use set instead of export:
    ```shell
    set FLASK_APP=app
    set FLASK_ENV=development
    flask run
    ```

- For Windows PowerShell, use `$env:` instead of `export:`
    ```shell
    $env:FLASK_APP = "app"
    $env:FLASK_ENV = "development"
    flask run
    ```
    
## Access the API
After startup the API, you would be able to send request to http://127.0.0.1:5000/\<certain_endpoint\>.

All valid endpoints and allow methods are posted below.

## Available Endpoints
Note: object_name can be client, event, location, supplier, suppy

#### For Simple Query
|        Endpoint       | Allowed Method | Description |
| :-------------------- | :------------: | :---------  |
| `/object_name/select` | GET, POST      | Get a list of objects in DB based on given properties in json form                            |
| `/object_name/update` | PUT            | Update existing objects to given value, return code 200 if success 400 if failed              |
| `/object_name/insert` | PUT            | Insert new objects into the DB with given values, return code 200 if success 400 if failed    |
| `/object_name/delete` | DELETE         | Delete new objects from the DB with given properties, return code 200 if success 400 if failed|

And for *supplier* and *supply* object, endpoints below are also available:

|            Endpoint          | Allowed Method | Description |
| :--------------------------- | :------------: | :---------  |
| `/object_name/<type>/select` | GET, POST      | Similar to the previous select, but just select object with given type |
| `/object_name/<type>/update` | PUT            | Similar to the previous update, but just update object with given type |
| `/object_name/<type>/insert` | PUT            | Similar to the previous update, but just insert object with given type |
| `/object_name/<type>/delete` | DELETE         | Similar to the previous update, but just delete object with given type |
\[type needs to be one of *entertain*, *decor* or *catering*\]

#### For complex Query
TBD

## Request body requirements
- For select

    If we want
    ```sql
    SELECT select_list FROM table_name WHERE condition;
    ```
    then request body should has the form:
    ```json
    {
      "where" : {
        "filed_name1" : "='val1'",
        "field_name2" : "<num",
        "field_name3" : "like 'val'"
      },
      "select" : ["select_field1", "select_field2"]
    }
    ```
    
- For update

    If we want
    ```sql
    UPDATE table_name SET set_name = val WHERE filed_name = val2
    ```
    then request body should has the form:
    ```json
    {
      "set" : {
        "set_name1" : "='val1'",
        "set_name2" : "=num"
      },
      "where" : {
        "field_name1" : "<val2",
        "field_name2" : "like 'val'"
      }
    }
    ```
- For insert

    If we want
    ```sql
    INSERT INTO tabel_name (field_name1, field_name2, ...) VALUES
    ('val1', 'val2', 105, ...);
    ```
    then request body should has the form:
    ```json
    {
      "into" : [ "field_name1", "field_name2", "filed_name3" ],
      "values" : [ "'val1'", "'val2'", 105 ]
    }
    ```
- For delete

    If we want
    ```sql
    DELETE FROM table_name WHERE filed_name = val2
    ```
    then request body should has the form:
    ```json
    {
      "where" : {
        "field_name1" : "<val2",
        "field_name2" : "like 'val'"
      }
    }
    ```
- For aggregation, join, group

    If we want
    ```sql
    SELECT FROM table1, table2 WHERE table1.filed_name = val2 GROUP BY table2.field_name HAVING table1.val3 > num
    ```
    then request body should has the form:
    ```json
    {
      "select": ["table1", "table2"],
      "where" : {
        "table1.field_name1" : "<val2",
        "table2.field_name2" : "like 'val'"
      },
      "group": ["table2.fieldname"],
      "have": {
        "table1.val3": "> num"
      }
    }
    ```

- For join

    Add one join field (and its corresonding by field) in request body like:
    ```json
    {
      ...,
      "join": "OUTER JOIN",
      "by": {
        "table1.val": "=table2.val"      
      }
    }
    ```
    then all tables will be connected using provied join in the from clause.

- For force command (I write this just in case if outer join does not work)

    **Please don't do this whenever possible, this is very hacky and should be deleted**
    
    *(But to be honest, the entire codebase I wrote is somewhat hacky ¯\\_(ツ)_/¯.)*

    Write a sql query with actual value replaced with {}, (e.g. SELECT * FROM Client WHERE ClientID = {})
    
    Put all value in a list with the order in query.
    
    Use request body
    ```json
    {
      "command": "SELECT * FROM Client WHERE ClientID = {} AND ClientFirstName = {}",
      "value": ["1", "'first_name'"]
    }
    ```