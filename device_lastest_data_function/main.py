# -*- coding:utf-8 -*-
import json
import logging
from .utils.unpack_meter import analysis_em_data, DataType, analysis_wm_data
from .utils.unpack_collector import analysis_collector_data
from datetime import datetime
from .settings.settings import THREE_PHASE_ELECTRIC_METER_PRODUCT_ID, PRODUCT_CATEGORY_ID_RT, \
    PRODUCT_CATEGORY_ID_WM, PRODUCT_CATEGORY_ID_EM, PRODUCT_CATEGORY_ID_CL

from .config import PGClient, MongoClient


def handler(event, context):
    """
    {
        "deviceType":2,
        "lineId":"",
        "enduserId":"5ce49e0a7qfrdxi3",
        "deviceId":"e5eb03047c2e11e994bb00163e04da1e",
        "command":{
            "action":"HWDevComm",
            "value":"C03201002018116102000019000000000000682600050900006891073334373533333308161ED0"
        },
        "reqId":"WEB-000009050026"
    }
    :param event: 
    :param context: 
    :return: 
    """

    logger = logging.getLogger()
    data = json.loads(event)
    collector_device_id = data.get("deviceId")
    device_type = data.get("deviceType")
    command = data.get("command")
    req_id = data.get('reqId', '')
    logging.info(f'handle:{event}')
    if not (req_id.startswith('WEB') or req_id.startswith('server')):
        return

    device_id = req_id.split('-')[1] if '-' in req_id else req_id.split('_')[1]

    # update data to online log
    try:
        client = PGClient()
        connect = client.connect()

        sql = f"""
            select d.product_id, d.project_id, d.device_id, pc.id, pc.name
                from device d 
                left join device d2 on d.parent_id =d2.id
                left join product p on p.product_id = d2.product_id
                left join product_category pc on p.category_id=pc.id 
                where d.device_id = '{device_id}' or d.dsn = '{device_id}';
        """
        with connect.cursor() as cursor:
            cursor.execute(sql)
            db_data = cursor.fetchall()
            if len(db_data):
                items = ('product_id', 'project_id', 'device_id', 'parent_category_id', 'parent_category_name')
                device_info = dict(zip(items, db_data[0]))
                repeater = True if device_info['parent_category_id'] == PRODUCT_CATEGORY_ID_RT else False
                three_phase = True if device_info['product_id'] in THREE_PHASE_ELECTRIC_METER_PRODUCT_ID else False
                device_analysis_data = {}
                if device_type == PRODUCT_CATEGORY_ID_EM:
                    analysis_data = analysis_em_data(data, repeater=repeater, three_phase=three_phase)
                    if not analysis_data:
                        logger.info(f'Types not supported for processing {event}, {context}')
                        return
                    analysis_data.pop('repeater_id')
                    analysis_data.pop('em_id')
                    analysis_data.pop('is_three_phase')

                    data_type = analysis_data.pop('data_type', None)
                    logger.info(f'analysis_data{analysis_data}')
                    for enum in DataType:
                        if int(enum) == data_type:
                            device_analysis_data = {enum.name: analysis_data}
                    logger.info(f'device_analysis_data{device_analysis_data}')
                elif device_type == PRODUCT_CATEGORY_ID_WM:
                    cumulative_flow, flow_rate, battery_voltage, status, dt, _ = analysis_wm_data(data,
                                                                                                  repeater=repeater)

                    device_analysis_data = {
                        'cumulative_flow': cumulative_flow,
                        'status': status,
                        'flow_rate': flow_rate,
                        'battery_voltage': battery_voltage,
                        'wm_device_time': dt

                    }
                elif device_type == PRODUCT_CATEGORY_ID_CL:
                    dt, signal_strength = analysis_collector_data(data)
                    device_analysis_data = {
                        'signal_strength': signal_strength,
                        'collector_device_time': dt
                    }
                else:
                    return

                mongo = MongoClient()
                db = mongo.db()
                collection = db['device_latest_data_instance']
                content = dict()
                content.update({
                    'device_id': device_id,
                    'project_id': device_info['project_id'],
                    'product_id': device_info['product_id'],
                    'category_id': device_type,
                    'update_time': datetime.now(),
                })
                device_data = collection.find_one({'device_id': device_id})  # 暂时调通数据，后改为原子操作
                if device_data:  #
                    device_analysis_data.update({'update_time': datetime.now()})
                    collection.update_many({'device_id': device_id}, {'$set': device_analysis_data})
                else:
                    content.update(device_analysis_data)
                    collection.insert_one(content)
                mongo.client.close()

    except Exception as e:
        logger.info(repr(e))

    print("status: success,", data)
    return "success"


if __name__ == "__main__":
    event = {"deviceName": "7e08d412cdfd11e8a22900163e0025b9", "action": "online"}
    context = {}
    ret = handler(event, context)
    print(ret)
