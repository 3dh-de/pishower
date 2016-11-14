#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import sys
import sqlite3
import logging

# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d.%m. %H:%M:%S')

logger = logging.getLogger()


class DBConnection:
    """ Convenient interface for SQLite3 db
    """
    _dbfile = "data.db"

    def __init__(self, fileName="data.db"):
        """ Init connection and db params """
        self._dbfile = fileName
        sqls = [
            'DROP TABLE IF EXISTS test',
            'CREATE TABLE test (i integer)',
            'INSERT INTO "test" VALUES(99)']
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

        sql = ""
        try:
            with sqlite3.connect(self._dbfile) as connection:
                cursor = connection.cursor()
                sql = "CREATE TABLE {0} ({1})".format(tableName, fieldStr)
                cursor.execute(sql)
                logger.debug('created table "{0}({1})"'.format(tableName, fieldStr))
                if primaryKey and not primaryKey.isspace():
                    sql = "CREATE UNIQUE INDEX index_{0}_{1} ON {0}({1})".format(tableName, primaryKey)
                    cursor.execute(sql)
                    logger.debug('created index for "{0}({1})"'.format(tableName, primaryKey))
        except sqlite3.OperationalError as err:
            logger.error("{0} for query: {1}".format(err, sql))
            return False
        return True

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

        try:
            with sqlite3.connect(self._dbfile) as connection:
                cursor = connection.cursor()
                cursor.execute("DROP TABLE {0}".format(tableName))
                logger.debug('deleted table "{0}"'.format(tableName))
        except sqlite3.OperationalError as err:
            logger.error(err)
            return False
        return True

    def tableExists(self, tableName):
        """ Check if given table exists

        Return True for existing table, False on any error
        """
        if tableName is None:
            logger.error('Invalid table name "{0}" given!'.format(tableName))
            return False

        try:
            with sqlite3.connect(self._dbfile) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT name FROM sqlite_master "
                    "WHERE type='table' AND name='{0}'".format(tableName))
                if cursor.fetchone() is None:
                    return False
        except sqlite3.OperationalError as err:
            logger.error(err)
            return False
        return True

    def _exec_queries(self, sqlQueries=[]):
        """ Execute given SQL statements

        Return results as one extended array
        """
        results = []
        if self._dbfile is None:
            logger.error(
                'Cannot execute SQL query! '
                'Database filename "{0}" invalid!'.format(self._dbfile))
            return results

        try:
            with sqlite3.connect(self._dbfile) as connection:
                cursor = connection.cursor()
                for sql in sqlQueries:
                    cursor.execute(sql)
                    logger.debug('executed query "{0}"'.format(sql))
                    for row in cursor:
                        results.extend(row)
                        logger.debug(
                            'added query "{0}" results "{1}" '
                            'to return value'.format(sql, row))
        except sqlite3.OperationalError as err:
            logger.error(err)
        return results


# Run minimal test
if __name__ == "__main__":
    db = DBConnection()
    if db.tableExists('user'):
        db.deleteTable('user')
    db.createTable('user', ['id INTEGER', 'name', 'firstname', 'age INTEGER'])

