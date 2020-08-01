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
from_conn = pymysql.connect('customer.mysql.database.chinacloudapi.cn', 'asiainfoadmin@customer', passwd='asiainfo@123',
                            db='customerportal')
"""
String url ="jdbc:mysql://ca-customer-portal.mysql.database.azure.com:3306/ca_customer_portal?useSSL=true&requireSSL=false"; myDbConn = DriverManager.getConnection(url, "cacpAdmin@ca-customer-portal", "!@#qwe123");
"""
to_conn = pymysql.connect('ca-customer-portal.mysql.database.azure.com', 'cacpAdmin@ca-customer-portal', passwd='!@#qwe123',
                          db='ca_customer_portal')

sql = """select  TSBFaultID, Reason from break_info"""
cursor = from_conn.cursor()

effect_row = cursor.execute(sql)
rows = cursor.fetchall()


to_cursor = to_conn.cursor()
for row in rows:
    insert_sql = """insert into break_info(TSBFaultID, Reason) values('%s', '%s')""" % (row[0], row[1])
    to_effect_row = to_cursor.execute(insert_sql)
    print(to_effect_row)
to_conn.commit()

print(time.time() - t)
