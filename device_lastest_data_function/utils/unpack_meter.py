from .unpack_meter_response import *
import abc
from enum import IntEnum
import logging

logger = logging.getLogger('script')


class DataType(IntEnum):
    energy = 1
    active_power = 2
    reactive_power = 3
    d_balance = 4


frame_analysts = []


def sub33reversebcdtoint(data_str):
    eq_list = [int("%x" % (int(data_str[index: index + 2], 16) - 0x33))
               for index in range(0, len(data_str), 2)]
    eq_list.reverse()  # 倒序
    ele = 0
    for one in eq_list:  # 拼接为十进制数
        ele = ele * 100 + one

    return ele


def register_analysts(cls):
    frame_analysts.append(cls)
    return cls


class AnalystsAbstract(metaclass=abc.ABCMeta):
    def __init__(self, is_three_phase=False):
        self.is_three_phase = is_three_phase

    @abc.abstractmethod
    def data_flag(self):
        """数据标示"""

    @abc.abstractmethod
    def data_type(self):
        """数据类型"""

    @abc.abstractmethod
    def make_analysis(self, data_str):
        """解析数据"""


@register_analysts
class TotalEnergy(AnalystsAbstract):
    @property
    def data_flag(self):
        """33333333 00000000"""
        return '33333333'

    @property
    def data_type(self):
        return DataType.energy.value

    def make_analysis(self, data_str):
        return {
            'data_type': self.data_type,
            'is_three_phase': self.is_three_phase,
            'total': round(sub33reversebcdtoint(data_str) * 0.01, 2)
        }


@register_analysts
class DeviceBalanceEnergy(AnalystsAbstract):
    @property
    def data_flag(self):
        """3335C333 00029000"""
        return '3335C333'

    @property
    def data_type(self):
        return DataType.d_balance.value

    def make_analysis(self, data_str):
        return {
            'data_type': self.data_type,
            'is_three_phase': self.is_three_phase,
            'd_balance': round(sub33reversebcdtoint(data_str) * 0.01, 2)
        }


@register_analysts
class ActivePower(AnalystsAbstract):
    @property
    def data_flag(self):
        """33343635 02030100"""
        return '33343635'

    @property
    def data_type(self):
        return DataType.active_power.value

    def make_analysis(self, data_str):
        return {
            'data_type': self.data_type,
            'is_three_phase': self.is_three_phase,
            'total': round(sub33reversebcdtoint(data_str) * 0.0001, 4)
        }


@register_analysts
class ThreePhaseActivePower(AnalystsAbstract):
    @property
    def data_flag(self):
        """33323635 0203ff00"""
        return '33323635'

    @property
    def data_type(self):
        return DataType.active_power.value

    def make_analysis(self, data_str):
        """33323635 0203ff00"""
        step = 6
        powers = [data_str[i:i + step] for i in range(0, len(data_str), step)]

        items = ['total', 'A', 'B', 'C']

        return {
            'data_type': self.data_type,
            'is_three_phase': self.is_three_phase,
            **dict(zip(items, [round(s * 0.0001, 4) for s in map(sub33reversebcdtoint, powers)]))
        }


@register_analysts
class ReactivePower(AnalystsAbstract):
    @property
    def data_flag(self):
        """33343735 02040100"""
        return '33343735'

    @property
    def data_type(self):
        return DataType.reactive_power.value

    def make_analysis(self, data_str):
        """"""
        active_power = sub33reversebcdtoint(data_str) * 0.0001

        return {
            'data_type': self.data_type,
            'is_three_phase': self.is_three_phase,
            'total': round(active_power, 4)
        }


@register_analysts
class ThreePhaseReactivePower(AnalystsAbstract):
    @property
    def data_flag(self):
        """33323735 00ff0302 """
        return '33323735'

    @property
    def data_type(self):
        return DataType.reactive_power.value

    def make_analysis(self, data_str):
        """ """
        step = 6
        powers = [data_str[i:i + step] for i in range(0, len(data_str), step)]
        for power in powers:
            sub33reversebcdtoint(power) * 0.0001

        items = ['total', 'A', 'B', 'C']

        return {
            'data_type': self.data_type,
            'is_three_phase': self.is_three_phase,
            **dict(zip(items, [round(s * 0.0001, 4) for s in map(sub33reversebcdtoint, powers)]))
        }


def analysis_em_data(data, repeater=False, three_phase=False):
    unpack_data = unpack_collector_data(data["command"]["value"])
    em_frame = unpack_data.data_area
    # 00 00 00 00 00 00  FEFEFEFE  688967452301006891083333333379333333A016
    offset = 0
    offset += 6 * 2  # pc地址
    repeater_id = None
    if repeater:
        repeater_id = em_frame[offset: offset + 4 * 2]
        offset += 4 * 2
        offset += 6 * 2  # 跳过功能码波特率参数

    cmd_data = em_frame[offset:]
    for index, item in enumerate(cmd_data):  # 过滤补充数据FE，找到电表数据的真正起始位置
        if cmd_data[index: index + 2] == "68":
            cmd_data = cmd_data[index:]
            break

    try:
        unpack_data = unpack_em_data(cmd_data)

        data_flag = unpack_data.data_area[:8]
        data_str = unpack_data.data_area[8:]

        for cls in frame_analysts:
            analysts = cls(is_three_phase=three_phase)
            if analysts.data_flag == data_flag:
                res = analysts.make_analysis(data_str)

                return {
                    'repeater_id': repeater_id,
                    'em_id': unpack_data.em_id,
                    **res
                }
    except Exception as e:
        logger.exception(f'data:{data}, repeater:{repeater}, three_phase:{three_phase}, e:{str(e)}')

    # # 电表数据为BCD编码，不可以直接按十进制处理:先按16进制减去填充数据0x33,
    # # 接着转为16进制字符串，再转为10进制，然后倒序，低字节为小数, 需要除以100
    # ele_quantity_str = unpack_data.data_area[8:]
    # eq_list = [int("%x" % (int(ele_quantity_str[index: index + 2], 16) - 0x33))
    #            for index in range(0, len(ele_quantity_str), 2)]  # 先每个字节按16进制减去填充数据0x33, 接着转为16进制字符串，再转为10进制数
    # eq_list.reverse()  # 倒序
    # ele_quantity = 0
    # print(eq_list)
    # for one in eq_list:  # 拼接为十进制数
    #     ele_quantity = ele_quantity * 100 + one
    # ele_quantity = ele_quantity / 100.0  # 最后两位为小数
    # print(ele_quantity)
    return None
