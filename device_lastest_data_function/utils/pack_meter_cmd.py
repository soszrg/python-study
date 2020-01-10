import datetime

DEVICE_TYPE_EM = 0  # 电表
DEVICE_TYPE_WM = 1  # 水表


class ElectricMeterCmd(object):
    """
    电表指令封装
    """
    begin = "68"  # 起始符
    end = "16"  # 结束符

    # 控制码
    CONTROL_CODE = {
        "close_em": "1C",
        "open_em": "1C"
    }
    SWITCH_CODE = {
        "close_em": "1A",
        "open_em": "1B"
    }

    def __init__(self, em_num, config=None, with_time=False):
        self.em_num = em_num
        self.config = config  # 项目配置
        self.with_time = with_time  # 指令是否带时间

    def _reverse_em_num(self):
        return reverse_byte(self.em_num)

    # 计算校验码
    @staticmethod
    def _crc(data):
        return em_crc(data)

    # 电表数据域每个字节需要加0x33
    @staticmethod
    def data_area_add_33(data_area):
        data_area = ["%02x" % (int(data_area[index: index + 2], 16) + 0x33) for index in range(0, len(data_area), 2)]

        return "".join(data_area)

    @property
    def open_em(self):
        return self.switch_em(do_open=True)

    @property
    def close_em(self):
        return self.switch_em()

    # 拉闸指令封装
    def switch_em(self, do_open=False):
        begin = ElectricMeterCmd.begin
        end = ElectricMeterCmd.end
        control_code = ElectricMeterCmd.CONTROL_CODE["open_em"] if do_open else ElectricMeterCmd.CONTROL_CODE["close_em"]
        if self.with_time:
            time = datetime.datetime.now()
            time += datetime.timedelta(hours=2)  # 时间需要大于表端时间，暂定当前后移2个小时
            year = "%d" % time.year
            valid_datetime = "%02d%02d%02d%02d%02d%s" % (time.second,
                                                         time.minute,
                                                         time.hour,
                                                         time.day,
                                                         time.month,
                                                         year[2:])
        else:
            valid_datetime = ""
        # 1A 关闸
        # 00 保留位
        switch_code = ElectricMeterCmd.SWITCH_CODE["open_em"] if do_open else ElectricMeterCmd.SWITCH_CODE["close_em"]
        data_area = self.config.em_operator_pwd + self.config.em_operator_code + switch_code + "00" + valid_datetime  # 数据域
        data_area = self.data_area_add_33(data_area)
        length = "%02x" % (len(data_area) // 2)  # 数据域长度
        em_data = begin + self._reverse_em_num() + begin + control_code + length + data_area
        em_data += "%02x" % em_crc(em_data) + end  # crc + end

        return em_data.upper()


class CollectorCmdBase(object):
    """
    采集器指令封装
    """
    begin = "C0"  # 起始符
    end = "D0"  # 结束符
    pc_addr = "000000000000"  # pc终端地址
    channel = "00"  # 通道号
    data_bit = "08"  # 数据位
    stop_bit = "01"  # 停止位
    check_bit = "02"  # 奇偶校验位

    # 类型码
    TYPE_CODE = {
        "server2collector": "31",  # 服务器到采集器
        "collector2server": "32"  # 采集器到服务器
    }

    # 功能码
    FUNC_CODE = {
        "wired_transmit": "02",  # 无线透传
        "wm_valve_control": "42",  # 写水表阀门控制
    }

    # 控制码
    CONTROL_CODE = {
        "success": "00",  # 命令处理成功
        "fail": "01",  # 命令处理失败
    }

    def __init__(self, collector_id, config=None, repeater=None):
        self.collector_id = collector_id
        self.config = config  # 项目配置
        self.repeater = repeater  # 中继地址

    @staticmethod
    def _crc(data):
        return cl_crc(data)


class Collector4ElectricMeter(CollectorCmdBase):
    """
    采集器包装电表指令
    """

    def __init__(self, collector_id, meter_data, config=None, repeater=None):
        self.meter_data = meter_data  # 表端数据
        super(Collector4ElectricMeter, self).__init__(collector_id, config=config, repeater=repeater)

    @property
    def em_cmd(self):
        if self.config:
            em_baud_rate = "%04x" % int(self.config.em_baud_rate)  # 十进制波特率字符串转为十六进制字符串
        else:
            em_baud_rate = "0960"  # 默认波特率

        em_type_code = self.TYPE_CODE["server2collector"]
        em_control_code = self.CONTROL_CODE["success"]
        if not self.repeater:  # 未使用中继
            em_func_code = self.FUNC_CODE["wired_transmit"]
            length = "%04x" % ((len(self.pc_addr) + len(self.channel) + len(em_baud_rate) + len(self.data_bit) + len(
                self.stop_bit) + len(self.check_bit) + len(self.meter_data)) // 2)

            cl_data = (self.begin + em_type_code + self.collector_id + em_func_code + em_control_code + length +
                       self.pc_addr + self.channel + em_baud_rate + self.data_bit + self.stop_bit + self.check_bit +
                       self.meter_data)
        else:
            em_baud_rate = em_baud_rate[-2:] + em_baud_rate[0:2]  # 波特率高低位转换
            cl_data = "C031%(collector_num)s3000%(length)s000000000000%(repeater)s" \
                      "%(func_num)s%(baud_rate)s%(data_bit)s%(stop_bit)s%(check_bit)s%(em_data)s" \
                      % {'collector_num': self.collector_id,  # 采集器表号
                         'length': "%04x" % (6 + len(self.repeater) // 2 + 6 + len(self.meter_data) // 2),  # 数据长度
                         'repeater': self.repeater,  # 中继器表号
                         'func_num': '00',  # 功能码
                         'baud_rate': em_baud_rate,  # 波特率(2400需要转为16进制，并低位在前)
                         "data_bit": "08",  # 数据位
                         'stop_bit': "01",  # 停止位
                         'check_bit': "02",  # 校验位
                         'em_data': self.meter_data,  # 电表指令
                         }

        cl_data += "%02xD0" % cl_crc(cl_data)
        print(cl_data)
        return cl_data.upper()


class Collector4WaterMeter(CollectorCmdBase):
    """
    采集器包装水表指令
    """

    def __init__(self, collector_id, wm_num, config=None, repeater=None):
        self.wm_num = wm_num  # 水表表号
        super(Collector4WaterMeter, self).__init__(collector_id, config=config, repeater=repeater)

    @property
    def wm_valve_close(self):
        return self._wm_valve_cmd()

    @property
    def wm_valve_open(self):
        return self._wm_valve_cmd(is_close=False)

    def _wm_valve_cmd(self, is_close=True):
        type_code = self.TYPE_CODE["server2collector"]
        control_code = self.CONTROL_CODE["success"]
        func_code = self.FUNC_CODE["wm_valve_control"]

        if is_close:
            valve_control = "%04x" % 0b10  # 关阀
        else:
            valve_control = "%04x" % 0b01  # 开阀

        length = "%04x" % ((len(self.pc_addr) + len(self.wm_num) + len(valve_control)) // 2)

        cl_data = (self.begin + type_code + self.collector_id + func_code + control_code + length +
                   self.pc_addr + self.wm_num + reverse_byte(valve_control))

        cl_data += "%02xD0" % cl_crc(cl_data)
        print(cl_data)
        return cl_data.upper()


# 采集器CRC校验码
def cl_crc(data):
    summary = 0
    index = 2

    while True:
        if index + 2 >= len(data):
            summary += int(data[index:], 16)
            break
        else:
            summary += int(data[index: index + 2], 16)
        index += 2

    return summary & 0xFF


# 电表CRC校验码
def em_crc(data):
    split_num = [int(data[index: index + 2], 16) for index in range(0, len(data), 2)]
    summary = sum(split_num)
    return summary & 0xFF


# 按字节逆序
def reverse_byte(data):
    split_str = [data[index: index + 2] for index in range(0, len(data), 2)]
    split_str.reverse()
    return "".join(split_str)


# 读水表指令封装
def wm_reading_cmd(collector_num, wm_num):
    data = "C031%s3100%04x000000000000%s" % (collector_num, 10, wm_num)
    data += "%02xD0" % cl_crc(data)
    return data.upper()


# 读电表指令封装
def em_reading_cmd(collector_num, em_num):
    em_data = "68%s68110433333333" % (reverse_byte(em_num),)
    em_data += "%02x16" % em_crc(em_data)

    cl_data = "C031%s0200%04x000000000000000960080102%s" % (collector_num, 6 + 6 + len(em_data) // 2, em_data)
    print(cl_data)
    print(cl_crc(cl_data))
    cl_data += "%02xD0" % cl_crc(cl_data)

    return cl_data.upper()


# 读电表指令封装(带中继)
def em_reading_cmd_with_repeater(collector_num, em_num, repeater=None, config=None):
    em_data = "68%s68110433333333" % (reverse_byte(em_num),)
    em_data += "%02x16" % em_crc(em_data)

    if config:
        em_baud_rate = "%04x" % int(config.em_baud_rate)  # 十进制波特率字符串转为十六进制字符串
    else:
        em_baud_rate = "0960"

    if not repeater:
        cl_data = "C031%s0200%04x00000000000000%s080102%s" \
                  % (collector_num, 6 + 6 + len(em_data) // 2, em_baud_rate, em_data)
        # cl_data = "C031%s0200%04x000000000000000960080102%s" % (collector_num, 6 + 6 + len(em_data) // 2, em_data)
    else:
        em_baud_rate = em_baud_rate[-2:] + em_baud_rate[0:2]  # 高低位转换
        cl_data = "C031%(collector_num)s3000%(length)s000000000000%(repeater)s" \
                  "%(func_num)s%(baud_rate)s%(data_bit)s%(stop_bit)s%(check_bit)s%(em_data)s" \
                  % {'collector_num': collector_num,  # 采集器表号
                     'length': "%04x" % (6 + len(repeater) // 2 + 6 + len(em_data) // 2),  # 数据长度
                     'repeater': repeater,  # 中继器表号
                     'func_num': '00',  # 功能码
                     'baud_rate': em_baud_rate,  # 波特率(2400需要转为16进制，并低位在前)
                     "data_bit": "08",  # 数据位
                     'stop_bit': "01",  # 停止位
                     'check_bit': "02",  # 校验位
                     'em_data': em_data,  # 电表指令
                     }

    print(cl_data)
    print(cl_crc(cl_data))
    cl_data += "%02xD0" % cl_crc(cl_data)

    return cl_data.upper()


# 电表关闸指令封装
def em_close_cmd_with_repeater(collector_num, em_num, repeater=None, config=None, with_time=False):
    # 电表指令封装
    em_data = ElectricMeterCmd(em_num, config, with_time).close_em
    return Collector4ElectricMeter(collector_num, meter_data=em_data, repeater=repeater, config=config).em_cmd


# 电表开闸指令封装
def em_open_cmd_with_repeater(collector_num, em_num, repeater=None, config=None, with_time=False):
    # 电表指令封装
    em_data = ElectricMeterCmd(em_num, config, with_time).open_em

    return Collector4ElectricMeter(collector_num, meter_data=em_data, repeater=repeater, config=config).em_cmd


# 水表关阀指令封装
def wm_close_cmd_with_repeater(collector_num, wm_num, repeater=None, config=None):
    # 水表指令封装
    return Collector4WaterMeter(collector_num, wm_num=wm_num, repeater=repeater, config=config).wm_valve_close


# 水表开阀指令封装
def wm_open_cmd_with_repeater(collector_num, wm_num, repeater=None, config=None):
    # 水表指令封装
    return Collector4WaterMeter(collector_num, wm_num=wm_num, repeater=repeater, config=config).wm_valve_open
