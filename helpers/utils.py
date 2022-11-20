import random
import string
import time
from datetime import datetime, timedelta
from urllib import parse

from selenium.common.exceptions import TimeoutException

from helpers.settings import SHORT_WAIT


def email_user(length=8) -> str:
    user = ''
    for x in range(length):
        user += random.choice(string.ascii_letters + string.digits)
    return str(f"{user}@autotest.ru")


def custom_date(delta=0, mobile=False) -> str:
    """
    Возвращает текущую дату в формате %d.%m.%Y
    :param delta: указывает смещение даты относительно текущего дня
    :param mobile: при указании параметра как True, вернет дату в формате %Y-%m-%d
    :return:
    """
    date = datetime.today() + timedelta(days=delta)
    if mobile:
        date = date.strftime('%Y-%m-%d')
    else:
        date = date.strftime('%d.%m.%Y')
    return str(date)


def random_number(length) -> str:
    """
    Возвращает строкой случайное число указанной длины
    :param length: указывает необходимую длину числа
    :return: string
    """
    if length == 0:
        length = 1
    range_start = 10 ** (length - 1)
    range_end = (10 ** length) - 1
    return str(random.randint(range_start, range_end))


def beautify_url(base_url, path):
    url_parts = list(parse.urlparse(base_url))
    url_parts[2] = path
    return parse.urlunparse(url_parts)


def try_to_retry(timeout=SHORT_WAIT, wait_time=0.1):
    def inner(fn):
        def wrapper(*args, **kwargs):
            finish_time = time.time() + timeout
            while True:
                try:
                    return fn(*args, **kwargs)
                except Exception as reason:
                    time.sleep(wait_time)
                    if time.time() > finish_time:
                        reason_message = str(reason)
                        reason_string = f'{reason.__class__.__name__}: {reason_message}'
                        failure = TimeoutException(f'''
Произошла ошибка, когда в течении {timeout} сек, с помощью page-object "{fn.__name__}", 
пытались взаимодествовать с локатором {args[1].by}="{args[1].path}"'
Причина ошибки: {reason_string}'''
                                                   )
                        raise failure

        return wrapper

    return inner
