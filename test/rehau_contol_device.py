# -*- encoding: utf-8 -*-
import requests


def device_control(work_mode):
    """
    :param work_mode: 0 auto; 1 manual; 4: night; 5 standby
    :return:
    """
    if not isinstance(work_mode, int):
        raise TypeError('work_mode type error: should be int!')

    if work_mode not in (0, 1, 4, 5):
        raise ValueError("work_mode value error!")

    url = "http://air.rehau.cn/web/h5/user/device-control"
    headers = {
        "Authorization": "token 30cad46266997e11a8787665aa215184b9d5b5152f8fee0b043206495073"
    }
    data = {
        "iot_id": "eSd44p4t5biqI56AI1R200101b9e00",
        "items": {
            "WorkMode": work_mode
        }
    }

    res = requests.post(url, json=data, headers=headers)
    if res.status_code != 200:
        raise Exception("server error: %s" % res.text)

    return res.text


if __name__ == '__main__':
    print device_control(5)
