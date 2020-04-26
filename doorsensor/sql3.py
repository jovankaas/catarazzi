#!/usr/bin/env python3

import sqlite3
import datetime
import os
import csv


def create_table_if_not_existing(database, table, fields):
    """
    """
    # Open the database.
    connection = sqlite3.connect(database)
    c = connection.cursor()

    query = '''CREATE TABLE IF NOT EXISTS ''' + table
    query += '''(''' + ''.join([str(k) + str(fields[k]) + ', ' for k in fields]) + ')'

    # Execute query:
    c.execute(query)
    # Confirm:
    connection.commit()
    # Close:
    connection.close()




def dict_from_dicts(dicts, keys):
    """(list of dicts, list of str)-> dict of dicts
    Return a dict of dicts which has the given keys
    as keys.
    >>> dicts = [{'hi':2, 'bye':3, 'it':5}]
    >>> dict_from_dicts(dicts, ['hi', 'bye'])
    {(2, 3): {'bye': 3, 'hi': 2, 'it': 5}}
    """

    d = {}
    if len(keys) == 1:
        for i in range(len(dicts)):
            d[dicts[i][keys[0]]] = dicts[i]
        return d
        #return {d[keys[0]]: d for d in dicts}
    for i in range(len(dicts)):
        d[tuple([dicts[i][key] for key in keys])] = dicts[i]
    return d


def dicts_from_db_table(database, table, constraints = {}, constraints_like = {}, constraints_less = {}, constraints_more = {}, verbose=False):
    """(str, str, [list of str])
    Return a list of dictionaries with column
    names as keys from a given table from the given
    database using the given constraints.
    """

    # Construct a valid query
    params = ""
    select = "select * from " + table
    select += " where " if constraints != {} or constraints_like != {} else ''
    for k in constraints:
        params = params + k + '=' + str(constraints[k]) + " and "
    for like in constraints_like:
        params = params + like + ' like ' + str(constraints_like[like]) + " and "
    for lessthan in constraints_less:
        params = params + lessthan + ' < ' + str(constraints_less[lessthan]) + " and "
    for morethan in constraints_more:
        params = params + morethan + ' > ' + str(constraints_more[morethan]) + " and "
    query = select + params[:-5]
    if verbose:
        print( query)

    # Open the database.
    connection = sqlite3.connect(database)
    c = connection.cursor()

    # Execute query and fetch column names and rows:
    c.execute(query)
    cols = [c.description[i][0] for i in range(len(c.description))]
    rows = c.fetchall()

    # Close connection without commit
    connection.close()

    # Transform data into dict:
    result = []
    for row in rows:
        summary = dict(zip(cols, row))
        result.append(summary)
    return result

def delete_from_db(constraints, database, table, confirm=True):
    """
    """
    # Make query
    params = ""
    delete = "delete from " + table
    delete += " where " if constraints != {} else ''
    for k in constraints:
        params = params + k + '=' + str(constraints[k]) + " and "
    query = delete + params[:-5]

    # Open the database.
    connection = sqlite3.connect(database)
    c = connection.cursor()

    print('Will now delete:', query)
    if confirm:
        if not raw_input('Is this ok? [No]/Sure ') == 'Sure':
            print('Will not delete. will exit program.')
            sys.exit()
    # Execute query:
    c.execute(query)
    # Confirm:
    connection.commit()
    # Close:
    connection.close()

def write_to_db(list_of_values, database, table, add_date=True, verbose = False):
    """(list of values, str, str) -> Nonetype
    Write to table in database the list of values.
    If number of values does not match table program
    will throw an error and exit.

    """

    # Check that the appropriate amount of values was given:
    length = len(list_of_values) + 1

    # Open the database.
    connection = sqlite3.connect(database)
    c = connection.cursor()

    # Add date to list of values
    if add_date:
        calculated_on = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        list_of_values.append(calculated_on)
    else:
        length -= 1
    field_values = tuple(list_of_values)

    if verbose:
        print('\n\nIn sql3.write_to_db:')
        print('length:', length)
        print('\nvalues to be written:', field_values)
        print('\nquery: INSERT INTO {table} VALUES ('.format(table=table) + (length - 1)* '?, ' + '?);')
        print('querysql: INSERT INTO ' + table + '(' + ''.join([str(val) + ',' for val in field_values]) + ');')
    # Insert into table and commit. Close the database.
    c.execute('INSERT INTO {table} VALUES ('.format(table=table) + (length - 1)* '?, ' + '?);', field_values)
    try:
        connection.commit()
    # Give a second chance if database is locked:
    except sqlite3.OperationalError as e:
        # try three times:
        if 'locked' in e:
            from time import sleep
            sleep(10)
            try:
                connection.commit()
            except sqlite3.OperationalError as e:
                sleep(20)
                try:
                    connection.commit()
                except sqlite3.OperationalError as e:
                    sleep(20)
                    connection.commit()
        else:
            raise
    connection.close()



def dict_to_db(dict_of_values, database, table, verbose=False):
    """
    Example from sqlite3 documentation on cursor:

    >>> conn = sqlite3.connect('example.db')
    >>> conn.row_factory = sqlite3.Row
    >>> c = conn.cursor()

    # Create a table
    >>> ex = c.execute('''CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)''')

    # Insert a row of data
    >>> ex = c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    # Save (commit) the changes
    >>> conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    >>> conn.close()


    >>> conn = sqlite3.connect('example.db')
    >>> c = conn.cursor()
    >>> cursorobj = c.execute('select * from stocks')
    >>> r = c.fetchone()
    >>> r
    (u'2006-01-05', u'BUY', u'RHAT', 100.0, 35.14)
    >>> len(r)
    5
    >>> r[2]
    u'RHAT'

    >>> conn.row_factory = sqlite3.Row
    >>> c = conn.cursor()
    >>> cursorobj = c.execute('select * from stocks')
    >>> r = c.fetchone()
    >>> type(r)
    <type 'sqlite3.Row'>
    >>> r.keys()
    ['date', 'trans', 'symbol', 'qty', 'price']
    >>> os.remove('example.db')
    """
    keys = table_keys(database, table, verbose)

    d = dict_of_values
    #print("table keys are:", keys)
    #print("dict keys are:", d.keys())
    list_of_values = [d[k] if k in d else None for k in keys]
    if verbose:
        print('\nList to be written:', list_of_values)

    write_to_db(list_of_values, database, table, add_date=False, verbose=verbose)


def table_keys(database, table, verbose=False):
    """
    Return table keys
    """
    # WTF:
    if ';' in table or ')' in table:
        return "What the fuck!?"

    # Open the database.
    connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row
    c = connection.cursor()

    # Fetch the keys.
    query = 'select * from ' + table
    if verbose:
        print('\n\nIn sql3.table_keys:')
        print('Database:', database, '-- table:', table, '-- query:', query)
    row = c.execute(query).fetchone()
    keys = [desc[0] for desc in c.description]
    if verbose:
        print('\n\nIn sql3.table_keys:')
        print('Database:', database, '-- table:', table, '-- keys:', keys)
    connection.close()

    #keys = row.keys()
    return keys


def add_fields(dicts_todb, db, tb, constraints, addfields, add_date=False):
    """
    Replace exising entry in database with new values, some of which are added
    to the older values.

    >>> conn = sqlite3.connect('example.db')
    >>> c = conn.cursor()
    >>> ex = c.execute('''CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)''')
    >>> ex = c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    >>> conn.commit()
    >>> conn.close()


    >>> conn = sqlite3.connect('example.db')
    >>> conn.row_factory = sqlite3.Row
    >>> c = conn.cursor()
    >>> new_vals = {'date': '2015-01-01', 'trans': 'BUY', 'symbol': 'RHAT', 'qty': 20, 'price': 7.03}
    >>> fields_to_be_added = ['qty', 'price']
    >>> cons = {'trans': '"BUY"', 'symbol': '"RHAT"'}
    >>> add_fields(new_vals, 'example.db', 'stocks', cons, fields_to_be_added)
    >>> cons['date'] = '"2015-01-01"'
    >>> dicts_from_db_table('example.db', 'stocks', cons)
    [{'date': u'2015-01-01', 'symbol': u'RHAT', 'trans': u'BUY', 'price': 42.17, 'qty': 120.0}]
    >>> os.remove('example.db')


    """
    ds = dicts_from_db_table(db, tb, constraints)
    if len(ds) > 1:
        print(" Warning: constraints are ambiguous. Multiple results from database. Will not write to database.")
        return None
    elif len(ds) < 1:
        print("No results found. Will place new results in database.")
        dict_to_db(dicts_todb, db, tb, add_date)
    else:
        d = ds[0]

        # Replace all old fields with new values:
        new = dicts_todb.copy()

        # Except for those fields that are to be added explicitly:
        for field in addfields:
            new[field] = d[field] + dicts_todb[field]
        dict_to_db(new, db, tb)


def dicts_from_file(filename):
    """
    Read text file and return table
    as list of dicts.
    """
    list_of_dicts = []
    csv.register_dialect('txtfile', delimiter=' ', skipinitialspace=True)

    with open(filename) as csvfile:
        line = csvfile.readline()
        keys = line.split()
        reader = csv.DictReader(csvfile, fieldnames=keys, dialect='txtfile')
        for row in reader:
            list_of_dicts.append(row)

    return list_of_dicts



def point_exists(database, table, parameters, verbose=False):
    '''(str, str, dict, bool) -> bool
    Search in the database if this point in
    parameter space for the specific point whether
    it already exists and return the boolean
    stating the answer.
    Parameters can be for example {"mzero": mzero, "mhalf": mhalf, "bin": bin} or
    {"mgo": mgo, "msq": msq, "mlsp": mlsp}.

    >>> testdb = 'example.db'
    >>> conn = sqlite3.connect(testdb)
    >>> c = conn.cursor()
    >>> t = c.execute('create table test_point_exists(mgo int, msq int, mlsp int, xsec real, ae real, n int)')
    >>> ex = c.execute('insert into test_point_exists values (?, ?, ?, ?, ?, ?)', (500, 600, 100, 0.0004, 0.02, 100000))
    >>> conn.commit()
    >>> conn.close()
    >>> point_exists(testdb, "test_point_exists", {'mgo': 500, 'msq': 600, 'mlsp': 100})
    True
    >>> os.remove('example.db')
    '''
    # Check if one is looking for a string, not a column:
    if 'proc_card' in parameters and '"' not in parameters['proc_card']:
        parameters['proc_card'] = '"' + parameters['proc_card'] + '"'
    # Open the database.
    connection = sqlite3.connect(database)
    c = connection.cursor()

    # Construct a query
    params = ""
    select = "select "
    if verbose:
        print(parameters)
    for k in parameters:
        params = params + k + '=' + str(parameters[k]) + " and "
        select += k + ', '
    #select += "n, ae from " + table
    select = select[:-2] + ' from ' + table
    query = select + " where " + params[:-5]
    # Execute query and fetch data
    if verbose:
        print(query)
    c.execute(query)
    data_entry = c.fetchone()
    if verbose:
        print(data_entry)
    # Close connection without commit
    connection.close()

    # Check if point exists.
    return data_entry != None and data_entry != []


if __name__ == '__main__':
    import doctest
    doctest.testmod()
