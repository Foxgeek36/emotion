# coding:utf8

"""
# @Time : 2019/12/7
# @Author : kylin
# @Desc: 自定义异常信息
"""

import traceback, os
from ez_utils import fls_log

flog = fls_log(log_name="")


def err_check(f):
    """
        装饰器函数
        -异常捕获装饰器-无返回值
    """

    def wrapper(*args, **kwargs):

        try:
            return f(*args, **kwargs)
        except Exception as e:
            print('Exception->', e)
            flog.log_error(os.path.relpath(f.__globals__['__file__']) + "." + f.__name__, traceback.format_exc())
            return None

    return wrapper
