import requests
from datetime import datetime
import os
import jdatetime
from PIL import Image
import time
import math

def check_finish_programm_time(finish_time):
    finish_time = finish_time.split(':')
    if int(datetime.now().hour) == int(finish_time[0]) and int(datetime.now().minute) == int(
            finish_time[1]) and int(datetime.now().second) > int(finish_time[2]):
        return True
    elif int(datetime.now().hour) == int(finish_time[0]) and int(datetime.now().minute) >= int(
            finish_time[1]):
        return True
    else:
        return False


def check_start_programm_time(start_time, finish_time):
    start_time = start_time.split(':')
    finish_time = finish_time.split(':')
    while True:
        if int(start_time[0]) < int(datetime.now().hour) <= int(finish_time[0]):
            if int(finish_time[0]) == int(datetime.now().hour):
                if int(datetime.now().minute) < int(finish_time[1]):
                    break
                elif int(datetime.now().minute) == int(finish_time[1]):
                    if int(datetime.now().second) < int(finish_time[2]):
                        break
            else:
                break
        if int(datetime.now().hour) == int(start_time[0]):
            if int(datetime.now().minute) > int(start_time[1]):
                break
        if int(datetime.now().hour) == int(start_time[0]):
            if int(datetime.now().minute) == int(start_time[1]):
                if int(datetime.now().second) > int(start_time[2]):
                    break
        if int(datetime.now().hour) == int(start_time[0]) and int(datetime.now().minute) == int(start_time[1]):
            if int(datetime.now().second) > int(start_time[2]):
                break


def convert_images_to_pdf(folder_path, file_name):
    image_list = os.listdir(folder_path)
    if len(image_list) != 0:
        image_file_list = []
        for img in image_list:
            img_file = Image.open('%s/%s' % (folder_path, img))
            image_file_list.append(
                img_file.convert('RGB')
            )
        image_file_list[0].save('%s/../%s.pdf' % (folder_path, file_name), save_all=True,
                                append_images=image_file_list)
    else:
        print('there is no images')


def jtoday_maker(date=None, string_date=False):
    if date is None:
        today = datetime.today()
        if string_date:
            return jdatetime.datetime.fromgregorian(datetime=today).strftime("%Y-%m-%d")
        else:
            return jdatetime.datetime.fromgregorian(datetime=today).strftime("%Y-%m-%d_%H-%M-%S")
    else:
        return jdatetime.datetime.fromgregorian(datetime=date)


def make_path(main_path, append_paths=None, file_name=None):
    if append_paths is None:
        append_paths = []
    if type(append_paths) is str:
        append_paths = [append_paths]
    assert type(append_paths) is list
    data_path = main_path
    for append_path in append_paths:
        data_path = '%s/%s' % (data_path, append_path)
        if not os.path.exists(data_path):
            os.mkdir(data_path)
    if file_name is not None:
        data_path = '%s/%s' % (data_path, file_name)
    return data_path


def remain_date(DateStr):
    fmt = '%m/%d/%Y'
    d2 = datetime.strptime(str(datetime.now().month) + '/' + str(datetime.now().day) + '/' + str(datetime.now().year),
                           fmt)
    d1 = DateStr
    return (d1 - d2).days


def root_path(path):
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), path)


def return_jdatetime_timestamp(date_string, format='%Y/%m/%d %H:%M:%S'):
    return jdatetime.datetime.strptime(date_string, format).timestamp()


def truncate(n, decimals=0, up=False):
    multiplier = 10 ** decimals
    if n % multiplier == 0:
        return n
    if up:
        return int((n / multiplier) + 1) * multiplier
    else:
        return int(n / multiplier) * multiplier


def round_truncate(number, step, _type="step"):
    if _type == "round":
        stepper = 10.0 ** step
        return math.trunc(stepper * number) / stepper
    elif _type == "step":
        temp = number / step
        output = math.floor(temp) * step
        if step < 1:
            return float(format(output, '.%sf' % abs(math.floor(math.log10(step)))))
        return output


def get_current_ip(proxies=None):
    session = requests.session()

    if proxies is None:
        session.proxies = {}
        session.proxies['http'] = 'socks5h://localhost:9050'
        session.proxies['https'] = 'socks5h://localhost:9050'
    else:
        session.proxies = proxies

    try:
        r = session.get('http://httpbin.org/ip')
    except Exception as e:
        print(str(e))
    else:
        return r.text


def renew_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="MyStr0n9P#D")
        controller.signal(Signal.NEWNYM)


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def date_time_into_timestamp(date_time):
    """
    converting nobitex date time into Timestamp datatype
    :param date_time: incoming datetime from Nobitex
    :return:
    """
    date_time = date_time.split('.')[0]
    return time.mktime(datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S").timetuple())
