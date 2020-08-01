from pprint import pprint

import pymysql

conn = pymysql.connect('escalatorpocdb.mysql.database.azure.com', 'cai@escalatorpocdb', passwd='1Q2w3e4r',
                       db='willtest')

province_sql = """select * from sl_areas where area_parent_id=0"""
city_sql = "select * from sl_areas where area_parent_id=%s and area_deep=2"
city_city_sql = "select * from sl_areas where area_parent_id=%s and area_deep=3"
cursor = conn.cursor()
cursor.execute(province_sql)
provinces_data = cursor.fetchall()
data = {}
for province_data in provinces_data:
    province_name = province_data[2]
    print(f"Parsing province {province_name}")
    province_id = province_data[1]
    cursor = conn.cursor()
    cursor.execute(city_sql % province_id)
    cities_data = cursor.fetchall()
    cities = []
    for city_data in cities_data:
        city_name = city_data[2]
        print(f"Parsing city {city_name}")
        city_id = city_data[1]
        cursor = conn.cursor()
        cursor.execute(city_city_sql % city_id)
        city_cities_data = cursor.fetchall()
        city_cities = []
        for city_city_data in city_cities_data:
            city_city_name = city_city_data[2]
            city_city_id = city_city_data[1]
            # cursor = conn.cursor()
            # cursor.execute(city_city_sql % city_city_id)
            # city_city_cities_data = cursor.fetchall()
            # if city_city_cities_data:
            #     city_cities.append({city_city_name: [one[2] for one in city_city_cities_data]})
            # else:
            city_cities.append(city_city_name)
        city = {city_name: city_cities}
        cities.append(city)
        print(city)
    data.update({province_name: cities})
pprint(data)
