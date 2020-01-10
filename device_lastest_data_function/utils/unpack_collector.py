from .unpack_meter import unpack_collector_data
import datetime


def analysis_collector_data(data):
    unpack_data = unpack_collector_data(data["command"]["value"])
    print(unpack_data)
    collector_data = unpack_data.data_area
    print(collector_data)
    time_area = collector_data[6 * 2:12 * 2]
    dt = datetime.datetime(
        year=int(time_area[0:1 * 2], 16) + 2000,
        month=int(time_area[1 * 2:2 * 2], 16),
        day=int(time_area[2 * 2:3 * 2], 16),
        hour=int(time_area[3 * 2:4 * 2], 16),
        minute=int(time_area[4 * 2:5 * 2], 16),
        second=int(time_area[5 * 2:6 * 2], 16)
    )
    signal_strength = int(collector_data[20 * 2:21 * 2], 16)
    return dt, signal_strength


"""
data = {
    "deviceType": 4,
    "lineId": "",
    "enduserId": "5ce49e0a7qfrdxi3",
    "deviceId": "e5eb03047c2e11e994bb00163e04da1e",
    "command": {
        "action": "HWDevComm",
        "value": "C0320100201811611300001D00000000000013070210291A7928D6D7005011611A00020613041C0900EAD0"
    },
    "reqId": "WEB-010020181161"
}
print(analysis_collector_data(data))
(datetime.datetime(19, 7, 2, 16, 41, 26), 26)
"""
