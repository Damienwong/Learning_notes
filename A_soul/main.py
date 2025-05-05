#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@func: 用于FT精准度、POD、反射率自动化测试
@author: WHB
@update:
"""

import time
from multiprocessing import Queue, Process
from zolix_motor_controller import MotorControl
import xlrd
import os
import pandas as pd
import numpy as np
from datetime import datetime
from FT_UDP_parser import FTUDPPARSE
from FT_ptc_sender import PTC_CMD
import math
import struct
from coordinate_trans import *
import matplotlib.pyplot as plt
import csv
import plotly as py
import plotly.express as px
from configparser import ConfigParser


class FtPerformance:
    def __init__(self):
        # 从Excel中读取配置文件
        # excel_dir = r'test_info.xlsx'
        # data = xlrd.open_workbook(excel_dir)
        # table = data.sheet_by_index(0)
        # self.sn = table.col_values(0)[1]
        # self.target_width = table.col_values(1)[1]
        # self.target_height = table.col_values(2)[1]
        # self.ground_true = table.col_values(3)[1]
        # self.com = table.col_values(4)[1]
        # self.pcap_flag = table.col_values(5)[1]
        # self.ref_true = table.col_values(6)[1]

        self.cfg = ConfigParser()
        self.cfg.read('test_config.ini', encoding='utf-8')
        self.sn = self.cfg.get('Range_test', 'lidar_sn')
        self.target_width = self.cfg.getfloat('Range_test', 'target_width')
        self.target_height = self.cfg.getfloat('Range_test', 'target_height')
        self.ground_true = self.cfg.getfloat('Range_test', 'ground_truth')
        self.com = self.cfg.get('Range_test', 'com')
        self.ref_true = self.cfg.getfloat('Range_test', 'target_ref')
        self.pcap_flag = 1


        self.points = 200

        # 转台初始化
        self.mc = MotorControl(self.com)
        self.mc.point_forward()

        # 点云解析初始化
        self.UDP = FTUDPPARSE('192.168.1.201', 2368)
        self.UDP.get_lidar_info_live()

        # PTC指令初始化
        self.PTC = PTC_CMD('192.168.1.201', 9347)
        self.PTC.ptc_command_get_inventory_info_A3V3()
        # 获取A3角度文件
        self.azimuth_adjust, self.elevation_adjust, self.df_correction = self.PTC.ptc_command_get_lidar_calibration_a3()

        # 设置文件保存文件夹的路径
        self.path = r'/home/hesai/Desktop/20230913_平面度测试/FT120C1X-B1-0361/2%/0.1m'.format(self.sn, datetime.now().strftime("%Y%m%d%H%M"))
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.pcap_dir = os.path.join(self.path, 'pcap_archive')
        if not os.path.exists(self.pcap_dir):
            os.mkdir(self.pcap_dir)
        self.raw_csv_dir = os.path.join(self.path, 'raw_data')
        if not os.path.exists(self.raw_csv_dir):
            os.mkdir(self.raw_csv_dir)

    def start_test(self, mid_azi):
        tic = time.time()
        # 根据目标板尺寸和距离获取转台姿态组合
        # 俯仰角度列表，单次俯仰停顿时间，[目标板有效水平FOV，目标板有效竖直FOV]
        color_list = ['bisque', 'forestgreen', 'royalblue', 'lightcoral', 'blueviolet', 'teal', 'olive', 'crimson',
                      'peru', 'bisque', 'forestgreen', 'royalblue', 'lightcoral', 'blueviolet', 'teal', 'olive', 'crimson',
                      'peru', 'bisque', 'forestgreen', 'royalblue', 'lightcoral', 'blueviolet', 'teal', 'olive', 'crimson',
                      'peru', 'bisque', 'forestgreen', 'royalblue', 'lightcoral', 'blueviolet', 'teal', 'olive', 'crimson',
                      'peru', 'bisque', 'forestgreen', 'royalblue', 'lightcoral', 'blueviolet', 'teal', 'olive', 'crimson',
                      'peru', 'bisque', 'forestgreen', 'royalblue', 'lightcoral', 'blueviolet', 'teal', 'olive', 'crimson',
                      'peru', 'bisque', 'forestgreen', 'royalblue', 'lightcoral', 'blueviolet', 'teal', 'olive', 'crimson',
                      'peru', 'bisque', 'forestgreen', 'royalblue', 'lightcoral', 'blueviolet', 'teal', 'olive', 'crimson',
                      'peru', 'bisque', 'forestgreen', 'royalblue', 'lightcoral', 'blueviolet', 'teal', 'olive', 'crimson',
                      'peru', 'bisque', 'forestgreen', 'royalblue', 'lightcoral', 'blueviolet', 'teal', 'olive', 'crimson',
                      'peru', 'bisque', 'forestgreen', 'royalblue', 'lightcoral', 'blueviolet', 'teal', 'olive', 'crimson',
                      'peru', 'bisque', 'forestgreen', 'royalblue', 'lightcoral', 'blueviolet', 'teal', 'olive', 'crimson',
                      'peru', 'bisque', 'forestgreen', 'royalblue', 'lightcoral', 'blueviolet', 'teal', 'olive', 'crimson',
                      'peru', 'bisque', 'forestgreen', 'royalblue', 'lightcoral', 'blueviolet', 'teal', 'olive', 'crimson',
                      'peru', 'bisque', 'forestgreen', 'royalblue', 'lightcoral', 'blueviolet', 'teal', 'olive', 'crimson',
                      'peru', ]
        fontsize = 18
        fig = plt.figure(figsize=(28, 28))
        fig.tight_layout()
        plt.subplots_adjust(wspace=0.2, hspace=0.25, right=0.8)
        ax = fig.add_subplot(211)
        bx = fig.add_subplot(212)
        bx.set_xlim(30, 150)
        bx.set_ylim(-40, 40)
        ax.set_title('{} Test Result @{}m Target: {}%'.format(self.sn, self.ground_true, self.ref_true), fontsize=fontsize)
        ax.set_xlabel('Azimuth(°)', fontsize=fontsize * 0.6)
        ax.set_ylabel('Elevation(°)', fontsize=fontsize * 0.6)
        ax.scatter(self.df_correction['Azimuth'], self.df_correction['Elevation'], s=7.5)
        ax.grid()
        result_csv = os.path.join(self.path, '{}_result_at_{}.csv'.format(self.sn, self.ground_true))
        write_csv_header(['Result_index', 'POD', 'Accuracy', 'Precision', 'Ref_Accuracy', 'Ref_Precision'], result_csv)

        yaw_pitch_list, seconds, target_valid_fov, pieces_pointing_list = self.field_slice()

        for i in range(len(yaw_pitch_list)):
            yaw = yaw_pitch_list[i][0]
            pitch = yaw_pitch_list[i][1]
            self.mc.moveByordr(yaw, 'X')
            self.mc.moveByordr(-pitch, 'Y')

            # 获取UDP数据
            datas = self.get_udp_data(seconds * 1600)

            # udp数据存为pcap
            pcap_name = r'yaw_{}_pitch_{}_second_{}_validhfov_{}_validvfov_{}_pointingazi_{}_pointingele_{}.pcap'.\
                format(yaw, pitch, seconds, target_valid_fov[0], target_valid_fov[1], pieces_pointing_list[i][0]+90,
                       pieces_pointing_list[i][1])
            pcap_path = os.path.join(self.pcap_dir, pcap_name)
            self.udp_to_pcap(datas, pcap_path)
            valid_point_data, df_unique = self.udp_data_process(datas, yaw, pitch, target_valid_fov[0], target_valid_fov[1], mid_azi)

            # 存三维点图，判定选点正确性
            valid_point_data_to_draw = valid_point_data[valid_point_data['distance'] < 30]
            df_valid = pd.DataFrame(valid_point_data_to_draw)
            fig = px.scatter_3d(df_valid, x='world_x', y='world_y', z='world_z', color='valid_flag',
                                hover_data=['column_id', 'channel_id', 'azimuth', 'elevation', 'distance'])
            fig.update_traces(marker_size=1)
            fig.update_layout(title='yaw_{}_pitch_{}_second_{}_validhfov_{}_validvfov_{}_pointingazi_{}_pointingele_{}'.
                              format(yaw, pitch, seconds, target_valid_fov[0], target_valid_fov[1], pieces_pointing_list[i][0]+90,
                       pieces_pointing_list[i][1]))
            pose_name = r'yaw_{}_pitch_{}_second_{}_validhfov_{}_validvfov_{}_pointingazi_{}_pointingele_{}.html'.\
                format(yaw, pitch, seconds, target_valid_fov[0], target_valid_fov[1], pieces_pointing_list[i][0]+90,
                       pieces_pointing_list[i][1])
            pose_dir = os.path.join(self.pcap_dir, pose_name)
            py.offline.plot(fig, filename=pose_dir, auto_open=False)


            ax.scatter(df_unique['azimuth'], df_unique['elevation'], s=7.5, color=color_list[i])
            ax.text(pieces_pointing_list[i][0]+90, pieces_pointing_list[i][1], str(i), color='Black', ha='center', va='center', size=30)
            pod, accuracy, precision, ref_accuracy, ref_precision = self.data_calculation(valid_point_data)

            if accuracy < 0.05 and precision < 0.05 and accuracy > -0.05:
                pass_flag = 1
            else:
                pass_flag = 0
            write_one_row_to_csv([i, pod, accuracy, precision, ref_accuracy, ref_precision], result_csv)

            result_color = ['Red', 'Black']
            bx.text(pieces_pointing_list[i][0] + 90, pieces_pointing_list[i][1],
                    '{} Result:\nPOD={}\nAccuracy={}\nPrecision={}\nRef_Accuracy={}\nRef_Precision={}'.
                    format(i, pod, accuracy, precision, ref_accuracy, ref_precision), color=result_color[pass_flag],
                    ha='center', va='center', size=10)

            print('水平{}  竖直{} 区域结果：\n'.format(yaw, pitch),
                  'POD： {}， 测距准度：{}， 测距精度：{}，反射率准度：{}，反射率精度：{}\n'.format(pod, accuracy, precision,
                                                                         ref_accuracy, ref_precision))
        pic_dir = os.path.join(self.path, '{}_result_at_{}.png'.format(self.sn, self.ground_true))
        plt.savefig(pic_dir)
        self.mc.point_forward()
        toc = time.time()
        print('测试结束，耗时：{}s'.format(round(toc-tic, 2)))


    def field_slice(self):
        """
        :func: 获取转台需要转动的姿态
        :return: 俯仰角度列表，单次俯仰停顿时间，[目标板有效水平FOV，目标板有效竖直FOV]
        """
        target_vfov = round(np.rad2deg(np.arctan(0.5 * self.target_height / self.ground_true)) * 2, 2)
        target_hfov = round(np.rad2deg(np.arctan(0.5 * self.target_width / self.ground_true)) * 2, 2)
        valid_vfov = min(target_vfov, 20)
        valid_hfov = min(target_hfov, 20)

        points_num_on_board = int(valid_vfov / 0.625) * int(valid_hfov / 0.625)
        frames = self.points / points_num_on_board
        seconds = math.ceil(frames / 10)

        v_piece_num = min(7, int(70 / min(target_vfov, 20)))
        h_piece_num = min(10, int(100 / min(target_hfov, 20)))

        # 垂直FOV切块
        v_list = []
        v_single_fov = int(70 / v_piece_num)
        if v_piece_num % 2:
            v_list.append(0)
            for i in range(v_piece_num // 2):
                v_list.append(round(float(0 + (i + 1) * v_single_fov), 1))
                v_list.append(round(float(0 - (i + 1) * v_single_fov), 1))
        else:
            for i in range(v_piece_num // 2):
                v_list.append(round(float(v_single_fov / 2 + i * v_single_fov), 1))
                v_list.append(round(float(-v_single_fov / 2 - i * v_single_fov), 1))

        # 水平FOV切块
        h_list = []
        h_single_fov = int(100 / h_piece_num)
        if h_piece_num % 2:
            h_list.append(0)
            for i in range(h_piece_num // 2):
                h_list.append(round(float(0 + (i + 1) * h_single_fov), 1))
                h_list.append(round(float(0 - (i + 1) * h_single_fov), 1))
        else:
            for i in range(h_piece_num // 2):
                h_list.append(round(float(h_single_fov / 2 + i * h_single_fov), 1))
                h_list.append(round(float(-h_single_fov / 2 - i * h_single_fov), 1))

        # 构建区域快中心线指向列表[[azi1, ele1], [azi2, ele2]...]
        pieces_pointing_list = []

        for v in sorted(v_list, reverse=True):
            for h in sorted(h_list):
                pieces_pointing_list.append([h, v])

        # 根据上述区域块中心线指向，求转台姿态组合列表
        yaw_pitchs = pointing_to_pose(pieces_pointing_list)
        print(pieces_pointing_list)
        print(yaw_pitchs)
        print('It need {} poses to obtain data, each takes {} seconds'.format(len(yaw_pitchs), seconds))
        return yaw_pitchs, seconds, [valid_hfov, valid_vfov], pieces_pointing_list

    def get_udp_data(self, udp_num):
        datas = []
        self.UDP.abandon_udp_data_in_cache()
        for _ in range(udp_num):
            data, addr = self.UDP.udpsock.recvfrom(int(self.UDP.data_size) + 42)
            datas.append(data)
        return datas

    def udp_to_pcap(self, udp_data, filepath):
        """
        :func: 把UDP数据存为pcap
        :param udp_data:
        :param filepath:
        :return:
        """
        PCAP_HEADER = 'd4c3b2a1020004000000000000000000ffff000001000000'
        PACKET_HEADER = '3d3505600dcf0c00'
        ETHERNET_HEADER_1 = 'ffffffffffff000a35001e5308004500'
        ETHERNET_HEADER_2 = 'cd2b4000401194cac0a801c9ffffffff27100940'
        udp_len_bi = struct.pack('<I', self.UDP.data_size + 42)
        # 16位的数据包头
        packet_header = bytes.fromhex(PACKET_HEADER) + udp_len_bi + udp_len_bi

        # ip包长
        ip_len_bin = struct.pack('>H', self.UDP.data_size + 28)
        # udp包长
        udp_bin = struct.pack('>H', self.UDP.data_size +8)

        # 构建mac首部+ip首bu+udp首部
        eth_header = bytes.fromhex(ETHERNET_HEADER_1) + ip_len_bin + bytes.fromhex(ETHERNET_HEADER_2) + udp_bin + \
              bytes.fromhex('0000')
        header = packet_header + eth_header
        dates = []
        for data in udp_data:
            dates.append(header)
            dates.append(data)
        buffer = b''.join(dates)
        with open(filepath, 'wb') as file_handle:
            file_handle.write(bytes.fromhex(PCAP_HEADER))
            file_handle.write(buffer)
        # print('{} saved.'.format(filepath))

    def udp_data_process(self, udp_data, yaw, pitch, valid_hfov, valid_vfov, mid_azi):
        valid_hfov_scope = [90 - 0.5 * valid_hfov, 90 + 0.5 * valid_hfov]
        valid_vfov_scope = [-0.5 * valid_vfov, 0.5 * valid_vfov]
        dataBytes = b''.join(udp_data)
        datas = np.frombuffer(dataBytes, dtype=self.UDP.ft_udp_dtype)
        point_num_per_udp = 120
        all_points_num = point_num_per_udp * len(datas)
        body_array_dtype = [('column_id',      'u2'     ),
                            ('channel_id',     'u2'     ),
                            ('dis_theory',     'float64'),
                            ('azimuth',        'float64'),
                            ('elevation',      'float64'),
                            ('distance',       'float64'),
                            ('reflectivity',   'u2'     ),
                            ('light',          'u2'     ),
                            ('confidence',     'u2'     ),
                            ('world_azi',      'float64'),
                            ('world_ele',      'float64'),
                            ('world_x',        'float64'),
                            ('world_y',        'float64'),
                            ('world_z',        'float64'),
                            ('valid_flag',     'u2'     ),
                            ]
        point_data = np.zeros(all_points_num, dtype=body_array_dtype)
        point_data['column_id'] = np.repeat(datas['column_id'], 120)
        point_data['channel_id'] = np.tile(np.arange(1, 121), len(datas))
        point_data['azimuth'] = self.azimuth_adjust[point_data['column_id'], point_data['channel_id'] - 1]
        point_data['elevation'] = self.elevation_adjust[point_data['column_id'], point_data['channel_id'] - 1]
        point_data['distance'] = datas['body']['block']['dis_ref_light_conf']['distance'].flatten() * 0.004
        point_data['reflectivity'] = datas['body']['block']['dis_ref_light_conf']['reflectivity'].flatten()
        point_data['light'] = datas['body']['block']['dis_ref_light_conf']['light'].flatten()
        point_data['confidence'] = datas['body']['block']['dis_ref_light_conf']['confidence'].flatten()

        point_data['dis_theory'] = np.repeat(1, len(datas)*point_num_per_udp)

        sph_lidar = np.array([point_data['dis_theory'], point_data['elevation'], point_data['azimuth']])
        sph_lidar = sph_lidar.T

        # 水平角度修正
        world_cordinate_temp = coordinate_rotation_sph(sph_lidar, 'z', mid_azi - 90)

        # 将雷达坐标系转化为大地坐标系，step1：俯仰
        world_cordinate_temp = coordinate_rotation_sph(world_cordinate_temp, 'y', pitch)

        # step2： 水平旋转
        world_cordinate = coordinate_rotation_sph(world_cordinate_temp, 'z', yaw)
        point_data['world_ele'] = world_cordinate[:, 1]
        point_data['world_azi'] = world_cordinate[:, 2]

        point_data['world_x'] = point_data['distance'] * np.cos(np.deg2rad(point_data['world_ele'])) * \
                                np.sin(np.deg2rad(point_data['world_azi']))
        point_data['world_y'] = point_data['distance'] * np.cos(np.deg2rad(point_data['world_ele'])) * \
                                np.cos(np.deg2rad(point_data['world_azi']))
        point_data['world_z'] = point_data['distance'] * np.sin(np.deg2rad(point_data['world_ele']))

        # 目标点的筛选
        # step1: 粗筛，保留边界外扩5度的数据
        valid_point_data = point_data[(point_data['world_azi'] > valid_hfov_scope[0] - 5) &
                                      (point_data['world_azi'] < valid_hfov_scope[1] + 5) &
                                      (point_data['world_ele'] > valid_vfov_scope[0] - 5) &
                                      (point_data['world_ele'] < valid_vfov_scope[1] + 5)
                                     ]
        valid_point_data['valid_flag'] = np.where(((valid_point_data['world_azi'] > valid_hfov_scope[0]) &
                                                   (valid_point_data['world_azi'] < valid_hfov_scope[1]) &
                                                   (valid_point_data['world_ele'] > valid_vfov_scope[0]) &
                                                   (valid_point_data['world_ele'] < valid_vfov_scope[1])), 1, 0)

        df = pd.DataFrame(valid_point_data, columns=['column_id', 'channel_id', 'dis_theory','azimuth', 'elevation', 'distance',
                                               'reflectivity', 'light', 'confidence', 'world_azi', 'world_ele',
                                               'world_x', 'world_y', 'world_z', 'valid_flag'])
        df1 = df.loc[df['valid_flag'] == 1]
        # 去重，保留唯一点画图
        df_scope = df1.drop_duplicates(subset=['column_id', 'channel_id'], keep='first', inplace=False) #, ignore_index=True)
        csv_path = os.path.join(self.raw_csv_dir, 'yaw_{}_pitch_{}_validhfov_{}_validvfov_{}.csv'.format(yaw, pitch,
                                                                                                         valid_hfov,
                                                                                                         valid_vfov))
        df.to_csv(csv_path)
        return valid_point_data, df_scope

    def data_calculation(self, valid_point_data):
        """
        :func: 计算测距POD、精准度；反射率精准度
        :param valid_point_data:
        :param valid_hfov:
        :param valid_vfov:
        :return:
        """
        # 选出参与计算的点，所有在视场范围内的点
        points_selected = valid_point_data[valid_point_data['valid_flag'] == 1]
        # 实际上靶的点，留下目标板前后20cm以内的点
        points_on_target = points_selected[(points_selected['world_x'] > (self.ground_true - 0.2)) &
                                           (points_selected['world_x'] < (self.ground_true + 0.2))]

        # 因为标定会使得目标板与大地x轴垂直，故这里的投影就是world_x

        # 准度
        accuracy = round(float(np.mean(points_on_target['world_x'] - self.ground_true)), 3)
        # 精度
        precision = round(float(np.std(points_on_target['world_x'] - self.ground_true, ddof=1)), 3)
        # POD
        pod = round((len(points_on_target) / len(points_selected)), 4)

        ref_accuracy = round(float(np.mean(points_on_target['reflectivity'] - self.ref_true)), 3)
        ref_precision = round(float(np.std(points_on_target['reflectivity'] - self.ref_true)), 3)
        return pod, accuracy, precision, ref_accuracy, ref_precision


def pointing_to_pose(azi_eles):
    """
    :func: 根据通道的指向，算出水平和俯仰转台需要旋转的角度
    :param azi_eles:
    :return:
    """
    yaw_pitchs = []  # [[水平角度1，俯仰角度1], [水平角度1，俯仰角度1], 。。。]
    for azi_ele in azi_eles:
        azi = azi_ele[0]
        ele = azi_ele[1]
        yaw = np.rad2deg(np.arcsin(np.sin(np.deg2rad(azi)) * np.cos(np.deg2rad(ele))))
        pitch = np.rad2deg(np.arctan(np.tan(np.deg2rad(ele)) / np.cos(np.deg2rad(azi))))
        yaw_pitchs.append([round(yaw, 1), round(pitch, 1)])
    return yaw_pitchs


def write_csv_header(header, savefile):
    with open(savefile, 'w', encoding='utf8', newline='') as csvfile:
        myWrite = csv.writer(csvfile)
        myWrite.writerow(header)


def write_one_row_to_csv(csv_row, savefile):
    with open(savefile, 'a+', encoding="utf8", newline="") as csvfile:
        myWriter = csv.writer(csvfile)
        myWriter.writerow(csv_row)


if __name__ == "__main__":
    FP = FtPerformance()
    mid_angle = float(input('请输入目标板中心Azimuth，并回车确认： '))
    FP.start_test(mid_angle)
