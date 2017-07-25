# MySQL usage example

from lib.db.db_mysql import Mysql

connector = Mysql()
connector.set_connection_details(host='79.78.159.149')

query = """
    select max(TimeStamp) from Data
"""

latest_data = connector.query(query, return_result=True)[0][0]

print(latest_data)