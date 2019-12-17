# coding:utf8

"""
[state]easy工具类/ 注意此处所限制的导出模块设置
-避免重名等误操作
"""

from .fls_log import fls_log

from .date_utils import fmt_date as fmt_date, get_day_n as after_date, get_seconds_n as after_seconds, \
    get_interval_day as interval_day, reformat_date_str as reformat_date_str

from .fmt_utils import allot_list

from .err_utils import err_check

# 在此处导入模块的配置/ 可以自由做添加及切换
from .err_log import Error