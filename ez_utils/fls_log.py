# coding:utf8
# Some Func About 'Write Log'
# Use: flog or fls_log(log_file)

import logging, os
from ez_utils.date_utils import fmt_date, FMT_DATE

'''
[state]自定义日志记录模块
-结合logger做完善
'''


def _get_msg4log(*args):
    """
        Get LOG msg/ 对输入的日志内容做判断
        -可加可不加 ->做灵活的操作
    """
    msg = ''
    try:
        if len(args) > 1:
            if "%" in args[0]:
                msg = args[0] % args[1:]
            else:
                msg = ' '.join([str(i) for i in args])
        elif len(args) == 1:
            msg = str(args[0])
        else:
            msg = ''
    except:
        pass
    return msg


class Fls_Log(object):

    # def __init__(self, log_filepath=None, file_name=None, date_name=fmt_date(fmt=FMT_DATE)[:8],
    def __init__(self, log_filepath=None, date_name=fmt_date(fmt=FMT_DATE)[:8],
                 # log_name='root', log_level=logging.DEBUG, show_console=True):
                 log_name='root', log_level=logging.INFO, show_console=False):
        """
            :param log_filepath: 日志存放路径
            :param file_name: 日志文件名称/ 冗余参数可做删除
            :param date_name:
            :param log_name:
            :param log_level: 初始为INFO日志格式
            :param show_console: 日志内容是否在终端做展示
        """

        # 若是无指定的日志存放路径则将日志存放至logs目录下
        if not log_filepath: log_filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
        # log_filepath不存在则做创建
        if not os.path.exists(log_filepath): os.makedirs(log_filepath)
        # if not file_name: file_name = "kylin"

        # 设置日志文件内容显示格式
        self.log_format = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)s] %(message)s'
        self.name = log_name
        self.log_filepath = os.path.join(log_filepath, self.name + '.log.' + date_name)  # 日志文件的绝对路径
        # Return a logger with the specified name
        self.logger = logging.getLogger(log_name)  # 创建指定名称的log对象
        self.handlers = self.logger.handlers  # 日志处理器/ 类别:FileHandler/StreamHandler/TimedRotatingFileHandler

        if not self.handlers:
            fh = logging.FileHandler(self.log_filepath, encoding="utf-8")  # 将日志内容保存至文件
            ch = logging.StreamHandler()  # 日志输出到流/ 此处是设置显示到终端

            # 设置日志内容显示格式/ 此处做精简直接上下结合配置到Formatter中 +--
            # fmt = "%(asctime)s %(levelname)s %(message)s"
            # if log_name: fmt = self.log_format
            # 文件内容显示格式
            formatter = logging.Formatter(fmt=self.log_format, datefmt=None)

            # 为handler指定输出格式
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            # logger添加的日志处理器
            self.logger.addHandler(fh)
            if show_console: self.logger.addHandler(ch)
            self.logger.setLevel(log_level)
            # self.handlers = self.logger.handlers  # 该设置是否是多余的? ---

    # 各日志级别设置 +--
    def log_info(self, *args):
        """
	        :param args: 所传的日志内容可以是多个
        """
        # Write info msg
        self.logger.info(_get_msg4log(*args))

    def log_debug(self, *args):
        # Write debug msg
        self.logger.debug(_get_msg4log(*args))

    def log_warning(self, *args):
        # Write warning msg
        self.logger.warning(_get_msg4log(*args))

    def log_error(self, *args):
        # Write error msg
        self.logger.error(_get_msg4log(*args))

    def log_critical(self, *args):
        # Write critical msg
        self.logger.critical(_get_msg4log(*args))


# def fls_log(log_filepath=None, file_name='kylin', log_name='root', show_console=False):
def fls_log(log_filepath=None, log_name='root', show_console=False):
    """
        生成日志文件对象的初始化操作
        :param log_filepath: 默认无日志文件目录/ 做自动生成完善 +--
        :param file_name: 日志文件名称/ 冗余的参数做注释
        :param log_name:
        :param show_console: 日志内容是否在终端做显示
        :return:
    """

    return Fls_Log(log_filepath=log_filepath,
                   # file_name=file_name,
                   log_name=log_name,
                   show_console=show_console)


if __name__ == '__main__':
    # ----For test
    a = fls_log()
    a.log_info('111')
    a.log_debug('222')
    a.log_warning('333')
    a.log_error('error:%s', 'test')
