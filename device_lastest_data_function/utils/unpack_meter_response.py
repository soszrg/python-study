# -*- encoding: utf-8 -*-
from collections import namedtuple
import datetime
from .pack_meter_cmd import reverse_byte

UnpackWm = namedtuple('UnpackWm', ['begin', 'type_code',
                                   'collector_id', 'func_code', 'control_code',
                                   'length', 'data_area',
                                   'check_code', 'end'])

UnpackEm = namedtuple('UnpackEm', ['begin_1', 'em_id',
                                   'begin_2', 'control_code',
                                   'length', 'data_area',
                                   'check_code', 'end'])


# 解析采集器数据包
def unpack_collector_data(data):
    if len(data) <= 14:
        raise Exception('data length error[%s]' % data)
    # todo verify crc

    offset = 0
    begin = data[offset: offset + 1 * 2]
    offset += 1 * 2
    type_code = data[offset: offset + 1 * 2]
    offset += 1 * 2
    collector_id = data[offset: offset + 6 * 2]
    offset += 6 * 2
    func_code = data[offset: offset + 1 * 2]
    offset += 1 * 2
    control_code = data[offset: offset + 1 * 2]
    offset += 1 * 2
    length = int(data[offset: offset + 2 * 2], 16)
    offset += 2 * 2
    data_area = data[offset: offset + length * 2]
    offset += length * 2
    check_code = data[offset: offset + 2 * 1]
    offset += 2 * 1
    end = data[offset:]

    return UnpackWm(begin, type_code, collector_id, func_code, control_code, length, data_area, check_code, end)


# 解析采集器数据包
def unpack_collector_data_with_repeater(data, repeater=False):
    if len(data) <= 14:
        raise Exception('data length error[%s]' % data)
    # todo verify crc

    offset = 0
    begin = data[offset: offset + 1 * 2]
    offset += 1 * 2
    type_code = data[offset: offset + 1 * 2]
    offset += 1 * 2
    collector_id = data[offset: offset + 6 * 2]
    offset += 6 * 2
    func_code = data[offset: offset + 1 * 2]
    offset += 1 * 2
    control_code = data[offset: offset + 1 * 2]
    offset += 1 * 2
    length = int(data[offset: offset + 2 * 2], 16)
    offset += 2 * 2
    data_area = data[offset: offset + length * 2]
    offset += length * 2
    check_code = data[offset: offset + 2 * 1]
    offset += 2 * 1
    end = data[offset:]

    return UnpackWm(begin, type_code, collector_id, func_code, control_code, length, data_area, check_code, end)


def analysis_wm_time(time_str):
    time_str = reverse_byte(time_str)
    time_int = int(time_str, 16)
    S = time_int & 0x3f
    M = (time_int & 0xfc0) >> 6
    H = (time_int & 0x1f000) >> 12
    d = (time_int & 0x3e0000) >> 17
    m = (time_int & 0x3c00000) >> 22
    Y = (time_int & 0xfc000000) >> 26
    return datetime.datetime(
        year=Y+2000,
        month=m,
        day=d,
        hour=H,
        minute=M,
        second=S
    )


# 解析读水表数据
def unpack_wm_reading_data(data):
    offset = 0
    # pc_addr = data[offset: offset+6*2]
    offset += 6 * 2
    wm_id = data[offset: offset + 4 * 2]
    offset += 4 * 2
    wm_data = data[offset:]

    dt = analysis_wm_time(wm_data[:4 * 2])

    unit_str = wm_data[4 * 2: (4 + 1) * 2]  # 单位
    unit = 0.1 ** (int(unit_str, 16) & 0x0F)

    cumulative_flow_str = wm_data[(4 + 1) * 2: (4 + 1 + 3) * 2]  # 累积流量
    cumulative_flow = int(reverse_byte(cumulative_flow_str), 16) * unit

    flow_rate_str = wm_data[14 * 2: (14 + 2) * 2]  # 瞬时流量 14-15 2字节
    flow_rate = int(reverse_byte(flow_rate_str), 16) * unit

    battery_voltage_str = wm_data[16 * 2: (16 + 1) * 2]  # 电池电压第15 字节 1个字节,unit 0.02V
    battery_voltage = int(battery_voltage_str, 16) * 0.02

    status_data = int(data[-2:], 16)

    print(unit)
    print(cumulative_flow)
    return cumulative_flow, flow_rate, battery_voltage, status_data, dt, wm_id,


# 解析水表数据
def analysis_wm_data(data, repeater=True):
    # 'C03201002018120131010006000000000000B6D0'
    # 'C0320100201812013100001C000000000000001820056911A940436400006400006400000000A5007FD0'
    unpack_data = unpack_collector_data(data["command"]["value"])

    wm_data = unpack_data.data_area
    cumulative_flow, flow_rate, battery_voltage, status_data, dt, wm_id = unpack_wm_reading_data(wm_data)
    print(cumulative_flow, status_data)
    status = []
    if status_data == 0:
        pass
    elif status_data == 0xFF:
        status = [1, 1, 1, 1, 1, 1]
    else:
        voltage_status = (status_data & 0x80) >> 7
        balance_status = (status_data & 0x40) >> 6
        mag_inter_record = (status_data & 0x20) >> 5
        mag_inter_now = (status_data & 0x10) >> 4
        sensor_status = (status_data & 0x0C) >> 2
        valve_status = status_data & 0x03
        status = [voltage_status, balance_status, mag_inter_record, mag_inter_now, sensor_status, valve_status]

    return cumulative_flow, flow_rate, battery_voltage, status, dt, wm_id


# 解析电表数据基本结构
def unpack_em_data(data):
    # 68 8967452301 00 68 91 08 3333333379333333 A0 16
    if len(data) < 32:
        raise Exception("data length error")
    offset = 0
    begin_1 = data[offset: offset + 1 * 2]
    offset += 1 * 2
    em_id = data[offset: offset + 6 * 2]
    em_id = reverse_byte(em_id)  # 原始数据中表号是按字节逆序的，需反序后才是真的表号
    offset += 6 * 2
    begin_2 = data[offset: offset + 1 * 2]
    offset += 1 * 2
    control_code = data[offset: offset + 1 * 2]
    offset += 1 * 2
    length = int(data[offset: offset + 1 * 2], 16)
    offset += 1 * 2
    data_area = data[offset: offset + length * 2]
    offset += length * 2
    check_code = data[offset: offset + 1 * 2]
    offset += 1 * 2
    end = data[offset:]

    return UnpackEm(begin_1, em_id, begin_2, control_code, length, data_area, check_code, end)


# 解析读电表累计电量数据
def unpack_em_electric_quantity_data(data, repeater=False):
    # 00 00 00 00 00 00  FEFEFEFE  688967452301006891083333333379333333A016
    offset = 0
    offset += 6 * 2  # pc地址
    if repeater:
        repeater_id = data[offset: offset + 4 * 2]
        offset += 4 * 2
        offset += 6 * 2  # 跳过功能码波特率参数

    cmd_data = data[offset:]
    for index, item in enumerate(cmd_data):  # 过滤补充数据FE，找到电表数据的真正起始位置
        if cmd_data[index: index + 2] == "68":
            cmd_data = cmd_data[index:]
            break
    unpack_data = unpack_em_data(cmd_data)
    ele_quantity_str = unpack_data.data_area[8:]
    # 电表数据为BCD编码，不可以直接按十进制处理:先按16进制减去填充数据0x33,
    # 接着转为16进制字符串，再转为10进制，然后倒序，低字节为小数, 需要除以100
    eq_list = [int("%x" % (int(ele_quantity_str[index: index + 2], 16) - 0x33))
               for index in range(0, len(ele_quantity_str), 2)]  # 先每个字节按16进制减去填充数据0x33, 接着转为16进制字符串，再转为10进制数
    eq_list.reverse()  # 倒序
    ele_quantity = 0
    print(eq_list)
    for one in eq_list:  # 拼接为十进制数
        ele_quantity = ele_quantity * 100 + one
    ele_quantity = ele_quantity / 100.0  # 最后两位为小数
    print(ele_quantity)

    return ele_quantity, unpack_data.em_id


# 解析电表数据
def analysis_em_data(data, repeater=False):
    # C0320100201812010200001E000000000000FEFEFEFE688967452301006891083333333379333333A016ECD0
    unpack_data = unpack_collector_data(data["command"]["value"])

    em_data = unpack_data.data_area
    return unpack_em_electric_quantity_data(em_data, repeater)
