# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import psycopg2

postgres_db = "fog_pub_test"
postgres_host = "postgresql.rdsg2q228keen9x.rds.gz.baidubce.com"
postgres_port = 3306
postgres_username = "pgadmin"
postgres_password = "zhrmghg_1949"

postgres_client = psycopg2.connect(database=postgres_db, user=postgres_username, password=postgres_password,
                                   host=postgres_host,
                                   port=postgres_port)
postgres_client.closed
postgres_client.close()
postgres_client
