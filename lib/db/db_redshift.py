import os
import sys
import psycopg2
from lib.load_config import Config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

"""
    Redshift database class
"""


class Redshift(Config):

    def __init__(self):
        super(Redshift, self).__init__()
        self._server = self.config['redshift']['server']
        self._db = self.config['redshift']['db']
        self._username = self.config['redshift']['username']
        self._password = self.config['redshift']['password']
        self._port = self.config['redshift']['port']

    def _open_connection(self):
        try:
            self._connection = psycopg2.connect(
                host=self._server,
                user=self._username,
                password=self._password,
                port=self._port,
                dbname=self._db
            )
        except psycopg2.OperationalError:
            raise

        self._cursor = self._connection.cursor()

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

        except psycopg2.ProgrammingError:
            if options['return_result']:
                return psycopg2.ProgrammingError
            raise

    def _close_connection(self):
        self._cursor.close()
        del self._cursor
        self._connection.close()

    def __exit__(self):
        self._close_connection()
