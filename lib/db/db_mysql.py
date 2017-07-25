import os
import sys
import pymysql
from lib.load_config import Config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

"""
    MySQL database class
"""


class Mysql(Config):

    def __init__(self):

        super(Mysql, self).__init__()
        try:
            self._username = self.config['mysql']['username']
        except KeyError:
            self._username = None
        try:
            self._password = self.config['mysql']['password']
        except KeyError:
            self._password = None
        try:
            self._server = self.config['mysql']['server']
        except KeyError:
            self._server = None
        try:
            self._port = self.config['mysql']['port']
        except KeyError:
            self._port = None
        try:
            self._db = self.config['mysql']['db']
        except KeyError:
            self._db = None

    def _open_connection(self):
        try:
            self._connection = pymysql.connect(
                host=self._server,
                user=self._username,
                password=self._password,
                port=self._port,
                db=self._db
            )
        except:
            raise

        self._cursor = self._connection.cursor()

    def set_connection_details(self, **kwargs):

        options = {
            'username': self._username,
            'password': self._password,
            'host': self._server,
            'port': self._port,
            'db': self._db
        }

        options.update(kwargs)

        self._username = options['username']
        self._password = options['password']
        self._server = options['host']
        self._port = options['port']
        self._db = options['db']

    def query(self, query_string, **kwargs):
        """
        :param query_string: This is the SQL query you want to execute
        :type query_string: ``str``
        :param kwargs: see below
        :return: Returns data from the input query, if called with return_result=True

        :Keyword Arguments:
            return_result (boolean): set to True to return queried data from a cursor (default True)
            commit (boolean): set to True to commit any changes to the database (default False)
        """

        options = {
            'return_result': True,
            'commit': False
        }

        options.update(kwargs)

        try:
            self._open_connection()

            self._cursor.execute(query_string)

            if options['return_result']:
                result = self._cursor.fetchall()
            if options['commit']:
                self._cursor.execute("commit")

            self._close_connection()

            if options['return_result']:
                return result

        except:
            raise

    def _close_connection(self):
        self._cursor.close()
        del self._cursor
        self._connection.close()

    def __exit__(self):
        self._close_connection()
