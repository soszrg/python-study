# import pymysql.cursors
# connection = pymysql.connect(host='escalatorpocdb.mysql.database.azure.com',
#                              user='cai@escalatorpocdb',
#                              password='1Q2w3e4r',
#                              db='db',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
#
# with connection.cursor() as cursor:
#     pass
import time

import pymysql

# engine=create_engine('mysql+pymysql://cai:1Q2w3e4r@escalatorpocdb.mysql.database.azure.com/escalator_poc')
t = time.time()
conn = pymysql.connect('escalatorpocdb.mysql.database.azure.com', 'cai@escalatorpocdb', passwd='1Q2w3e4r',
                       db='escalator_poc')

sql = """select * from otis_unit_escalator"""
cursor = conn.cursor()

effect_row = cursor.execute(sql)
print(cursor.fetchall())
print(time.time()-t)
