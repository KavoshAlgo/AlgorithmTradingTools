import requests
from datetime import datetime
import os
import jdatetime
import time
import math
import sys
import asyncio
import ssl

SSL_PROTOCOLS = (asyncio.sslproto.SSLProtocol,)
try:
    import uvloop.loop
except ImportError:
    pass
else:
    SSL_PROTOCOLS = (*SSL_PROTOCOLS, uvloop.loop.SSLProtocol)


def ignore_aiohttp_ssl_error(loop):
    """Ignore aiohttp #3535 / cpython #13548 issue with SSL data after close

    There is an issue in Python 3.7 up to 3.7.3 that over-reports a
    ssl.SSLError fatal error (ssl.SSLError: [SSL: KRB5_S_INIT] application data
    after close notify (_ssl.c:2609)) after we are already done with the
    connection. See GitHub issues aio-libs/aiohttp#3535 and
    python/cpython#13548.

    Given a loop, this sets up an exception handler that ignores this specific
    exception, but passes everything else on to the previous exception handler
    this one replaces.

    Checks for fixed Python versions, disabling itself when running on 3.7.4+
    or 3.8.

    """
    if sys.version_info >= (3, 7, 4):
        return

    orig_handler = loop.get_exception_handler()

    def ignore_ssl_error(loop, context):
        if context.get("message") in {
            "SSL error in data received",
            "Fatal error on transport",
        }:
            # validate we have the right exception, transport and protocol
            exception = context.get('exception')
            protocol = context.get('protocol')
            if (
                    isinstance(exception, ssl.SSLError)
                    and exception.reason == 'KRB5_S_INIT'
                    and isinstance(protocol, SSL_PROTOCOLS)
            ):
                if loop.get_debug():
                    asyncio.log.logger.debug('Ignoring asyncio SSL KRB5_S_INIT error')
                return
        if orig_handler is not None:
            orig_handler(loop, context)
        else:
            loop.default_exception_handler(context)

    loop.set_exception_handler(ignore_ssl_error)


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
            import decimal
            return decimal.Decimal(format(output, '.%sf' % abs(math.floor(math.log10(step)))))
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
