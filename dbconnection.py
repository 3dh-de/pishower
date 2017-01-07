#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" PiShower project
    @copyright  Christian Daehn (c) 2006, http://3dh.de
    @license    MIT license
"""

import sqlite3
from pishowerutils import logger


class DBConnection:
    """ Convenient interface for SQLite3 db """
    _dbfile = 'data.db'

    def __init__(self, fileName='data.db'):
        """ Init connection and db params """
        self._dbfile = fileName
        sqls = [
            'DROP TABLE IF EXISTS test',
            'CREATE TABLE test (i integer)',
            'INSERT INTO \'test\' VALUES(99)']
        self._exec_queries(sqls)
        return

    def __del__(self):
        pass

    def createTable(self, tableName, fields, primaryKey=""):
        """ Create a table of given name with given fields

        name   = SQLite table name, MUST NOT contain special chars+whitespaces
        fields = array of SQL table field names and type:
                 e.g.: ['id INTEGER', 'msg', 'price REAL', 'name TEXT']

        Return True on successs, False on any error
        """
        if tableName is None:
            logger.error('Invalid table name "{0}" given!'.format(tableName))
            return False
        if fields is None:
            logger.error('Invalid table fields "{0}" given!'.format(fields))
            return False

        if self.tableExists(tableName) is True:
            logger.warning(
                'DB table "{0}" cannot be created! '
                'Table already exists!'.format(tableName))
            return False

        fieldStr = None
        for field in fields:
            if fieldStr is None:
                fieldStr = '{0}'.format(field)
            else:
                fieldStr = '{0}, {1}'.format(fieldStr, field)

        sqls = []
        sqls.append('CREATE TABLE {0} ({1})'.format(tableName, fieldStr))
        if primaryKey and not primaryKey.isspace():
            sqls.append('CREATE UNIQUE INDEX index_{0}_{1} '
                        'ON {0}({1})'.format(tableName, primaryKey))
        retval = self._exec_queries(sqls)
        return True if retval is not None else False

    def deleteTable(self, tableName):
        """ Delete the given table

        Return True on success, False on any error
        """
        if tableName is None:
            logger.error('Invalid table name "{0}" given!'.format(tableName))
            return False

        if self.tableExists(tableName) is False:
            logger.warning(
                'DB table "{0}" cannot be deleted! '
                'Table does not exist!'.format(tableName))
            return False

        sqls = ['DROP TABLE {0}'.format(tableName)]
        retval = self._exec_queries(sqls)
        return True if retval is not None else False

    def tableExists(self, tableName):
        """ Check if given table exists

        Return True for existing table, False on any error
        """
        if tableName is None:
            logger.error('Invalid table name "{0}" given!'.format(tableName))
            return False

        sqls = ['SELECT name FROM sqlite_master '
                'WHERE type=\'table\' AND name=\'{0}\''.format(tableName)]
        retval = self._exec_queries(sqls)
        return True if len(retval) and retval[0] is not None else False

    def writeEntry(self, tableName, primaryKey, values={}):
        """ Insert or update a table entry with given values

        tableName  - name of target table for insert/update of entry
        primaryKey - name of table primary key or selector column
        values     - dictionary with field:value pairs of entry to write

        Return True on success, False on any error
        """
        if tableName is None:
            logger.error('Invalid table name given!')
            return False

        if primaryKey is None:
            logger.error('Invalid table entry primary key given!')
            return False

        if values is False or primaryKey not in values:
            logger.error('Invalid table entry primary key given!')
            return False

        id = values[primaryKey]

        if self.tableExists(tableName) is False:
            logger.warning(
                'Entry cannot be written! '
                'Table does not exist!'.format(tableName))
            return False

        sqls = ['SELECT * FROM {0} WHERE {1} '
                '= \'{2}\''.format(tableName, primaryKey, id)]
        retval = self._exec_queries(sqls)
        if len(retval) and retval[0] is not None:
            logger.debug('Updating entry {0}="{1}"'.format(primaryKey, id))
            sqls = ['UPDATE {0} SET {1} WHERE {2} = \'{3}\''.format(tableName,
                    ', '.join("%s='%s'" % (k, v) for k, v in values.items()),
                                                                    primaryKey, id)]
        else:
            logger.debug('Inserting new entry {0}="{1}"'.format(primaryKey, id))
            sqls = ['INSERT INTO {0} ({1}) VALUES ({2})'.format(tableName,
                    ', '.join("{0}".format(k) for k in values.keys()), 
                    ', '.join("'{0}'".format(values[k]) for k in values.keys()))]

        retval = self._exec_queries(sqls)
        return True if retval is not None else False

    def _exec_queries(self, sqlQueries=[]):
        """ Execute given SQL statements

        Return results as one extended array
        """
        results = []
        sql = ""
        if self._dbfile is None:
            logger.error(
                'Cannot execute SQL query! '
                'Database filename "{0}" invalid!'.format(self._dbfile))
            return results

        try:
            with sqlite3.connect(self._dbfile) as connection:
                cursor = connection.cursor()
                for query in sqlQueries:
                    sql = query
                    for row in cursor.execute(sql):
                        results.append(row)
                        if 0:
                            logger.debug(
                                'added query "{0}" results "{1}" '
                                'to return value'.format(sql, row))
                    logger.debug('executed query "{0}"'.format(sql))
        except sqlite3.OperationalError as err:
            logger.error('{0}! query: {1}'.format(err, sql))
            return None
        return results


# Run minimal test
if __name__ == '__main__':
    db = DBConnection()
    if db.tableExists('user'):
        db.deleteTable('user')
    else:
        logger.error('check for existing table failed!')
    db.createTable('user', ['id INTEGER', 'name', 'firstname', 'age INTEGER'])

    db.writeEntry('user', 'id', {'id': 2, 'name': 'Wurst', 'firstname': 'Hans', 'age': 24})
    db.writeEntry('user', 'id', {'id': 2, 'name': 'Wurst', 'firstname': 'Hänschen', 'age': 30})
