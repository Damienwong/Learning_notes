#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: haibo.wang
@Date: 2025/7/26
@Description: 
"""

import logging
import os.path
import sys
from logging.handlers import RotatingFileHandler
from datetime import datetime


class MyLogger:
    def __init__(self, module_name, log_dir=''):
        self.module_name = module_name
        self.log_dir = log_dir
        self.all_logs_dir = os.path.join(log_dir, 'all_logs')
        self.err_logs_dir = os.path.join(log_dir, 'err_logs')

        current_date = datetime.now().strftime('%Y%m%d')

        # 创建日志记录器
        self.logger = logging.getLogger(f"{module_name}_{current_date}")
        self.logger.setLevel(logging.DEBUG)  # 设置最低日志级别

        # 清除可能存在的旧处理器
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 所有日志的处理器
        all_log_filename = os.path.join(self.all_logs_dir, f'{current_date}_{module_name}.log')
        all_handler = RotatingFileHandler(
            all_log_filename,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding='utf-8'
        )
        all_handler.setLevel(logging.DEBUG)
        all_handler.setFormatter(formatter)
        self.logger.addHandler(all_handler)

        # 错误日志的处理器
        err_log_filename = os.path.join(self.err_logs_dir, f'{current_date}_{module_name}.log')
        err_handler = RotatingFileHandler(
            err_log_filename,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding='utf-8'
        )
        err_handler.setLevel(logging.ERROR)
        err_handler.setFormatter(formatter)
        self.logger.addHandler(err_handler)

        # 控制台处理器
        console_handle = logging.StreamHandler(sys.stdout)
        console_handle.setLevel(logging.INFO)
        console_handle.setFormatter(formatter)
        self.logger.addHandler(console_handle)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message, exc_info=False):
        self.logger.error(message, exc_info=exc_info)  # True: 包含异常信息 False: 不包含异常信息

    def critical(self, message, exc_info=False):
        self.logger.critical(message, exc_info=exc_info)

    def exception(self, message):
        """
        记录异常信息（包含堆栈跟踪）
        :param message:
        """
        self.logger.exception(message)

    def log(self, level, message, exc_info=False):
        """
        通用日志记录方法
        :param level:
        :param message:
        :param exc_info:
        """
        self.logger.log(level, message, exc_info=exc_info)

    def get_log_file_path(self):
        """
        获取当前日志文件路径
        """
        current_date = datetime.now().strftime('%Y%m%d')
        return {
            'all_logs': os.path.join(self.all_logs_dir, f"{current_date}_{self.module_name}.log"),
            'err_logs': os.path.join(self.err_logs_dir, f"{current_date}_{self.module_name}.log")
        }


if __name__ == '__main__':
    mylog = MyLogger('test')

    # 获取日志文件路径
    log_paths = mylog.get_log_file_path()
    print('所有日志文件：{}'.format(log_paths['all_logs']))
    print('错误日志文件：{}'.format(log_paths['err_logs']))

    mylog.debug('这是一条调试信息。')
    mylog.info('这是 一条普通信息。')
    mylog.warning('这是一条警告信息。')
    mylog.error('这是一条错误信息')
    mylog.critical('这是一条严重错误信息')

    # 记录异常信息
    try:
        1 / 0
    except Exception as e:
        # mylog.exception('发生了一个除零异常')
        # 等价于
        mylog.error('发生了一个除零异常', exc_info=True)

    # 通用日志方法
    mylog.log(logging.INFO, '使用通用方法记录的信息')

    # 模拟一个长时间运行的任务
    for i in range(100):
        mylog.info('任务进度：{}%'.format(i))

        if i == 50:
            mylog.warning('任务进度过半')

        if i == 90:
            try:
                open('somthing.txt')
            except Exception as e:
                mylog.exception('文件操作失败')