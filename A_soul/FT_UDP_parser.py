# -*- coding: UTF-8 -*-


import socket
import os
import struct
import time
from datetime import datetime
import csv
from collections import defaultdict
import pandas as pd
import numpy as np
from queue import Queue
from threading import Thread


ft_10hz_time_list = [
    0.65,   1.95,   3.25,   4.55,   5.85,   7.15,   15.45,  16.75,
    18.05,  19.35,  20.65,  21.95,  23.25,  24.55,  25.85,  27.15,
    28.45,  29.75,  31.05,  39.35,  40.65,  41.95,  43.25,  44.55,
    45.85,  47.15,  48.45,  49.75,  51.05,  52.35,  53.65,  54.95,
    56.25,  64.55,  65.85,  67.15,  68.45,  69.75,  71.05,  72.35,
    73.65,  74.95,  76.25,  77.55,  78.85,  80.15,  88.45,  89.75,
    91.05,  92.35,  93.65,  94.95,  96.25,  97.55 ]

ft_ideal_angle_list = [
    40.31,  40.93,  41.56,  42.18,  42.81,  43.43,  44.06,  44.68,
    45.31,  45.93,  46.56,  47.18,  47.81,  48.43,  49.06,  49.68,
    50.31,  50.93,  51.56,  52.18,  52.81,  53.43,  54.06,  54.68,
    55.31,  55.93,  56.56,  57.18,  57.81,  58.43,  59.06,  59.68,
    60.31,  60.93,  61.56,  62.18,  62.81,  63.43,  64.06,  64.68,
    65.31,  65.93,  66.56,  67.18,  67.81,  68.43,  69.06,  69.68,
    70.31,  70.94,  71.56,  72.19,  72.81,  73.44,  74.06,  74.69,
    75.31,  75.94,  76.56,  77.19,  77.81,  78.44,  79.06,  79.69,
    80.31,  80.94,  81.56,  82.19,  82.81,  83.44,  84.06,  84.69,
    85.31,  85.94,  86.56,  87.19,  87.81,  88.44,  89.06,  89.69,
    90.31,  90.94,  91.56,  92.19,  92.81,  93.44,  94.06,  94.69,
    95.31,  95.94,  96.56,  97.19,  97.81,  98.44,  99.06,  99.69,
    100.31, 100.94, 101.56, 102.19, 102.81, 103.44, 104.06, 104.69,
    105.31, 105.94, 106.56, 107.19, 107.81, 108.44, 109.06, 109.69,
    110.32, 110.94, 111.57, 112.19, 112.82, 113.44, 114.07, 114.69,
    115.32, 115.94, 116.57, 117.19, 117.82, 118.44, 119.07, 119.69,
    120.32, 120.94, 121.57, 122.19, 122.82, 123.44, 124.07, 124.69,
    125.32, 125.94, 126.57, 127.19, 127.82, 128.44, 129.07, 129.69,
    130.32, 130.94, 131.57, 132.19, 132.82, 133.44, 134.07, 134.69,
    135.32, 135.94, 136.57, 137.19, 137.82, 138.44, 139.07, 139.69 ]


class FTUDPPARSE:

    def __init__(self, host='', port=2368, multicast_flag=False, network_card=''):
        self.host = host
        self.port = port
        self.ft_udp_dtype = np.dtype([
            ('Pre_header+Header', '<S25'),
            ('body', [('block', [('dis_ref_light_conf', [('distance', '<u2'), ('reflectivity', '<u1'), ('light', '<u1'),
                                                         ('confidence', '<u1')], 120)])]),
            ('reserved', '<S7'),
            ('column_id', '<u2'),
            ('ending', '<S40'),
        ])
        self.multicast_flag = multicast_flag
        self.network_card = network_card

    def get_lidar_info_live(self):
        self.udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if self.network_card != '':
            try:
                self.udpsock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, self.network_card.encode('utf-8'))
                print('已绑定网卡：{}'.format(self.network_card))
            except Exception as e:
                print('绑定网卡失败：{}'.format(self.network_card))
                input('继续吗？')

        try:
            if self.multicast_flag:
                self.udpsock.bind(('', self.port))
                multicast_group = "239.127.3.1"  # 组播组地址
                interface_ip = "172.16.35.98"  # 接口IP地址
                self.udpsock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                                      socket.inet_aton(multicast_group) + socket.inet_aton(interface_ip))
            else:
                self.udpsock.bind(('', self.port))
        except OSError as e:
            print('端口已被占用，检查是否有其他程序占用端口！')
            command = "netstat -tunlp | grep 2368 | awk '{print $6}' | cut -f 1 -d '/'"
            print('占用端口的进程号如下：')
            os.system(command)
            print('尝试使用【kill -9 进程号】关闭进程！')
            return b''
        self.udpsock.settimeout(180)
        data = b''
        for _ in range(10):
            data, addr = self.udpsock.recvfrom(1000)
            if len(data) > 600:
                break
        self.data_size = len(data)
        pre_header = struct.unpack('<6B', data[: 6])
        ee, ff, protocol_version_major, protocol_version_minor, reserved_version, reserved = pre_header
        # print(pre_header)
        self.udp_protocol_version = protocol_version_major + round(protocol_version_minor / 10, 1)
        header = struct.unpack('<HHBBBBBH', data[6: 17])
        self.col_num, self.row_num, col_resolution, row_resolution, first_block_return, dist_unit, block_index, \
        self.channel_num = header
        # print(header)
        self.col_resolution = col_resolution * 0.01
        self.row_resolution = row_resolution * 0.01
        if self.udp_protocol_version == 7.1:
            self.background_light_len = 2
            self.body_size = 6 * 120
            self.body_start_idx = 6 + 19
            self.tail_start_idx = 6 + 19 + self.body_size
            return_mode_id = data[self.tail_start_idx + 11]
            self.return_mode = {51: 'Strongest Return',
                                58: 'First and Strongest Return'}[return_mode_id]
        elif self.udp_protocol_version == 7.2:
            self.background_light_len = 1
            self.body_size = 5 * 120
            self.body_start_idx = 6 + 19
            self.tail_start_idx = 6 + 19 + self.body_size
            return_mode_id = data[self.tail_start_idx + 11]
            self.return_mode = {51: 'First Return',
                                55: 'Strongest Return',
                                60: 'First and Strongest Return'}[return_mode_id]
        # print(return_mode_id, self.return_mode)
        self.frame_period = struct.unpack('<H', data[self.tail_start_idx + 12: self.tail_start_idx + 14])[0]
        if self.udp_protocol_version == 7.1 or self.udp_protocol_version == 7.2:
            self.lidar_type = 'FT120'
        print('Get Lidar info successfully.\n',
              '          Lidar Type: {}.\n'.format(self.lidar_type),
              '     UDP Data Length: {}.\n'.format(self.data_size),
              'UDP Protocol Version: {}.\n'.format(self.udp_protocol_version),
              '    Reserved Version: {}.\n'.format(reserved_version),
              ' Total Column Number: {}.\n'.format(self.col_num),
              '    Total Row Number: {}.\n'.format(self.row_num),
              '   Column Resolution: {}°.\n'.format(self.col_resolution),
              '      Row Resolution: {}°.\n'.format(self.row_resolution),
              '         Return Mode: {}.\n'.format(self.return_mode),
              '        Frame Period: {}ms.\n'.format(self.frame_period))
        return 1

    def get_lidar_info_from_pcap(self, pcap_file):
        first_data = self.pick_out_first_udp(pcap_file)
        self.data_size = len(first_data)
        pre_header = struct.unpack('<6B', first_data[: 6])
        ee, ff, protocol_version_major, protocol_version_minor, reserved_version, reserved = pre_header
        # print(pre_header)
        self.udp_protocol_version = protocol_version_major + round(protocol_version_minor / 10, 1)
        header = struct.unpack('<HHBBBBBH', first_data[6: 17])
        self.col_num, self.row_num, col_resolution, row_resolution, first_block_return, dist_unit, block_index, \
        self.channel_num = header
        # print(header)
        self.col_resolution = col_resolution * 0.01
        self.row_resolution = row_resolution * 0.01
        if self.udp_protocol_version == 7.1:
            self.background_light_len = 2
            self.body_size = 6 * 120
            self.body_start_idx = 6 + 19
            self.tail_start_idx = 6 + 19 + self.body_size
            return_mode_id = first_data[self.tail_start_idx + 11]
            self.return_mode = {51: 'Strongest Return',
                                58: 'First and Strongest Return'}[return_mode_id]
        elif self.udp_protocol_version == 7.2:
            self.background_light_len = 1
            self.body_size = 5 * 120
            self.body_start_idx = 6 + 19
            self.tail_start_idx = 6 + 19 + self.body_size
            return_mode_id = first_data[self.tail_start_idx + 11]
            self.return_mode = {51: 'First Return',
                                55: 'Strongest Return',
                                60: 'First and Strongest Return'}[return_mode_id]
        # print(return_mode_id, self.return_mode)
        self.frame_period = struct.unpack('<H', first_data[self.tail_start_idx + 12: self.tail_start_idx + 14])[0]
        self.first_data = first_data
        if self.udp_protocol_version == 7.1 or self.udp_protocol_version == 7.2:
            self.lidar_type = 'FT120'
        print('Get Lidar info successfully.\n',
              '          Lidar Type: {}.\n'.format(self.lidar_type),
              '     UDP Data Length: {}.\n'.format(self.data_size),
              'UDP Protocol Version: {}.\n'.format(self.udp_protocol_version),
              '    Reserved Version: {}.\n'.format(reserved_version),
              ' Total Column Number: {}.\n'.format(self.col_num),
              '    Total Row Number: {}.\n'.format(self.row_num),
              '   Column Resolution: {}°.\n'.format(self.col_resolution),
              '      Row Resolution: {}°.\n'.format(self.row_resolution),
              '         Return Mode: {}.\n'.format(self.return_mode),
              '        Frame Period: {}ms.\n'.format(self.frame_period))

    def pick_out_first_udp(self, file):
        with open(file, 'rb') as file_handle:
            for data_type, data, first_point_cloud in self.pcap_data_to_generator(file_handle):
                if data_type == 'u' and first_point_cloud == 1:
                    return data
                else:
                    pass

    def pcap_data_to_generator(self, file_handle):
        first_flag = 1
        file_header = 24
        package_header = 16
        mac_header = 14
        ip_header = 20
        udp_header = 8
        while True:
            if first_flag:
                header = file_handle.read(file_header + package_header + mac_header + ip_header)
                date_type = header[file_header + package_header + mac_header + 9]
                if date_type == 17:  # UDP(17)
                    udp_head_data = file_handle.read(udp_header)
                    first_data_size = struct.unpack('>H', udp_head_data[-4: -2])[0] - 8
                    first_data = file_handle.read(first_data_size)
                    if first_data[0: 2] == b'\xee\xff':
                        print('Got the First Point Cloud UDP.')
                        first_flag = 0
                        point_cloud_udp_flag = 1
                        yield 'u', first_data, point_cloud_udp_flag
                    else:
                        print('Data No.{} is NOT point cloud udp.'.format(first_flag))
                        first_flag = 0
                        point_cloud_udp_flag = 0
                        yield 'u', first_data, point_cloud_udp_flag
                else:
                    length_ipheader_data = int.from_bytes(header[56: 58], byteorder='big')
                    ip_data = length_ipheader_data - ip_header
                    first_data = file_handle.read(ip_data)
                    print('Data No.{} is NOT udp.'.format(first_flag))
                    first_flag = 0
                    point_cloud_udp_flag = 0
                    yield 't', first_data, point_cloud_udp_flag
            else:
                # 非第一包
                header = file_handle.read(package_header + mac_header + ip_header)
                try:
                    date_type = header[16 + 23]
                except (struct.error, IndexError):
                    print('{} data left. Parsing is done'.format(len(header)))
                    return
                if date_type == 17:
                    udp_head_data = file_handle.read(udp_header)
                    date_size = struct.unpack('>H', udp_head_data[-4: -2])[0] - 8
                    data = file_handle.read(date_size)
                    if data[0: 2] == b'\xee\xff':
                        yield 'u', data, 1
                    else:
                        yield 'u', data, 0
                else:
                    length_ipheader_data = int.from_bytes(header[32: 34], byteorder='big')
                    ip_data = length_ipheader_data - ip_header
                    data = file_handle.read(ip_data)
                    yield 't', data, 0

    def abandon_udp_data_in_cache(self):
        for idx in range(1000):
            t0 = time.time()
            for _ in range(103):
                data, addr = self.udpsock.recvfrom(int(self.data_size) + 42)
            t1 = time.time()
            if (t1 - t0) * 1e4 > 100:
                # print("there are about {} udp datas in cache".format(103 * idx))
                return
        print("there are over 101000 udp datas in cache, please check your cache size")
        return

    def parse_FT_tail(self, data):
        reserved1_dict = {0: 'ANALOG_1V0',
                          1: 'ANALOG_3V3',
                          2: 'ANALOG_5V0',
                          3: 'ANALOG_1V8',
                          4: 'ANALOG_DN_TST_V_1V8_RX',
                          5: 'ANALOG_DC_TST_I_1V8_RX',
                          6: 'ANALOG_PWRIN_VOL',
                          7: 'ANALOG_LASER_HV',
                          8: 'ANALOG_SPAD_HV',
                          9: 'ANALOG_1V24_FPGA',
                          10: 'ANALOG_0V8_MCU',
                          11: 'ANALOG_1V2_POWER_TRX_1',
                          12: 'ANALOG_1V2_POWER_TRX_2',
                          13: 'ANALOG_1V35_POWER_TRX',
                          14: 'ANALOG_1V5_POWER_TRX',
                          15: 'ANALOG_1V6_POWER_TRX',
                          16: 'ANALOG_VOUT_HVCUR',
                          17: 'ANALOG_MPB_NTC1',
                          18: 'ANALOG_MPB_NTC2',
                          19: 'ANALOG_TSENSOR0_1V8_RX',
                          20: 'ANALOG_TRX_NTC1',
                          21: 'ANALOG_TRX_NTC2',
                          22: 'ANALOG_PD_OUT_TRX',
                          23: 'ANALOG_0V8_FPGA',
                          24: 'STARTUP_CNT0',
                          25: 'STARTUP_CNT1',
                          26: 'STARTUP_CNT2',
                          27: 'STARTUP_CNT3',
                          28: 'FPGA_Temp',
                          29: 'MCU_Temp',
                          30: 'ANALOG_3V3_AUX',
                          31: 'CS_CK',
                          32: 'CS_CK_ERR_0',
                          33: 'CS_CK_ERR_1'
                          }
        value_type = [[i for i in range(5)] + [i for i in range(6, 17)] + [22, 23, 30],
                      [5] + [i for i in range(17, 22)] + [28, 29],
                      [i for i in range(24, 28)]]
        tail_dict = {}
        tail_dict['Starter'] = data[0: 2]
        tail_dict['Protocol_version'] = data[2] + data[3] / 10
        tail_dict['Reserved1_version'] = data[4]
        tail_dict['Total_Col_Num'] = struct.unpack('<H', data[6: 8])[0]
        tail_dict['Total_Row_Num'] = struct.unpack('<H', data[8: 10])[0]
        tail_dict['Column_Resolution'] = data[10] * 0.01
        tail_dict['Row_Resolution'] = data[11] * 0.01
        tail_dict['First_Block_Return'] = data[12]
        tail_dict['Dist_Unit'] = data[13]
        tail_dict['Channel_Num'] = struct.unpack('<H', data[15: 17])[0]
        reserved1_id = data[self.tail_start_idx + 2]
        tail_dict['Reserved1_ID'] = reserved1_id
        tail_dict['Reserved1_item'] = reserved1_dict[reserved1_id]
        if reserved1_id in value_type[0]:
            Reserved1_value = struct.unpack('<H', data[self.tail_start_idx: self.tail_start_idx + 2])[0] / 2 ** 9
            tail_dict['Reserved1_value'] = round(Reserved1_value, 3)
        elif reserved1_id in value_type[1]:
            Reserved1_value = struct.unpack('<h', data[self.tail_start_idx: self.tail_start_idx + 2])[0] / 2 ** 7
            tail_dict['Reserved1_value'] = round(Reserved1_value, 3)
        elif reserved1_id == 31:
            tail_dict['Reserved1_value'] = str(data[self.tail_start_idx + 1]) + ',' + str(data[self.tail_start_idx])
        elif reserved1_id == 32:
            value_int = int.from_bytes(data[self.tail_start_idx: self.tail_start_idx + 2], byteorder='little', signed=False)
            tail_dict['Reserved1_value'] = 'BANK2:{}, BANK1:{}, BANK0:{}'.format(value_int >> 10 & 0b11111,
                                                                                 value_int >> 5 & 0b11111,
                                                                                 value_int & 0b11111)
        elif reserved1_id == 33:
            value_int = int.from_bytes(data[self.tail_start_idx: self.tail_start_idx + 2], byteorder='little', signed=False)
            tail_dict['Reserved1_value'] = 'BANK5:{}, BANK4:{}, BANK3:{}'.format(value_int >> 10 & 0b11111,
                                                                                 value_int >> 5 & 0b11111,
                                                                                 value_int & 0b11111)
        else:
            tail_dict['Reserved1_value'] = struct.unpack('<H', data[self.tail_start_idx: self.tail_start_idx + 2])[0]
        tail_dict['Reserved2'] = data[self.tail_start_idx + 3: self.tail_start_idx + 3 + 4]
        tail_dict['Column_ID'] = struct.unpack('<H', data[self.tail_start_idx + 7: self.tail_start_idx + 7 + 2])[0]
        tail_dict['Frame_ID'] = data[self.tail_start_idx + 9]
        tail_dict['Working_mode'] = data[self.tail_start_idx + 10]
        return_mode_id = data[self.tail_start_idx + 11]
        tail_dict['Return_mode'] = {51: 'First Return',
                                    55: 'Strongest Return',
                                    60: 'First and Strongest Return'}[return_mode_id]
        tail_dict['Frame_period'] = struct.unpack('<H', data[self.tail_start_idx + 12: self.tail_start_idx + 12 + 2])[0]
        # 纯秒计时
        temp1, temp2 = struct.unpack('>IH', data[self.tail_start_idx + 14: self.tail_start_idx + 20])
        utc_sec = temp1 * 2 ** 16 + temp2
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(utc_sec))

        # 年月日时分秒计时
        # utc = struct.unpack('<6B', data[self.tail_start_idx + 14: self.tail_start_idx + 20])
        # year, month, day, hour, minite, second = utc
        # year += 1900
        # if month == 0 or day == 0:
        #     dt = 0
        #     utc_sec = 0
        # else:
        #     dt = datetime(year, month, day, hour, minite, second)
        #     utc_sec = dt.timestamp()
        tail_dict['UTC_time'] = dt
        timestamp = struct.unpack('<I', data[self.tail_start_idx + 20: self.tail_start_idx + 20 + 4])[0]
        tail_dict['Timestamp'] = timestamp
        tail_dict['UTC_timestamp'] = utc_sec + timestamp * 1 / 1000000
        tail_dict['Factory_info'] = hex(data[self.tail_start_idx + 24])
        tail_dict['Sequence_num'] = struct.unpack('<I', data[self.tail_start_idx + 25: self.tail_start_idx + 25 + 4])[0]
        # print(tail_dict)
        return tail_dict

    def parse_FT_body(self, data):
        body_data = data[25: 25 + self.body_size]
        body_dict = defaultdict(list)
        chn_len = 4 + self.background_light_len
        body_dict['Column_ID'].append(self.parse_FT_tail(data)['Column_ID'])
        for i in range(self.channel_num):
            dis = struct.unpack('<H', body_data[i * chn_len: i * chn_len + 2])[0]
            dis = round(dis * 0.004, 3)
            ref = body_data[i * chn_len + 2]
            if self.background_light_len == 1:
                backing = body_data[i * chn_len + 3]
            else:
                backing = struct.unpack('<H', body_data[i * chn_len + 3: i * chn_len + 5])[0]
            confidence = body_data[i * chn_len + 3 + self.background_light_len]
            body_dict['dist'].append(dis)
            body_dict['ref'].append(ref)
            body_dict['background_light'].append(backing)
            body_dict['conf'].append(confidence)

        # print(body_dict)
        return body_dict


def udp_tail_live(udp_num, save_path, host='192.168.1.205', port=2365):
    FTUDP = FTUDPPARSE(host, port)
    FTUDP.get_lidar_info_live()
    FTUDP.abandon_udp_data_in_cache()
    data, addr = FTUDP.udpsock.recvfrom(int(FTUDP.data_size) + 42)
    tail_dict = FTUDP.parse_FT_tail(data)
    csv_header = list(tail_dict.keys())
    savedir = os.path.join(save_path, r'tail_data_{}.csv'.format(datetime.now().strftime("%Y%m%d%H%M")))
    write_csv_header(csv_header, savedir)
    csv_rows = []
    datas = []
    FTUDP.abandon_udp_data_in_cache()
    for _ in range(udp_num):
        data, addr = FTUDP.udpsock.recvfrom(int(FTUDP.data_size) + 42)
        datas.append(data)
    for data in datas:
        tail_dict = FTUDP.parse_FT_tail(data)
        tail_value_list = list(tail_dict.values())
        csv_rows.append(tail_value_list)
    write_n_row_to_csv(csv_rows, savedir)


def udp_tail_live_long(time_sec, save_path, host='', port=2368):
    FTUDP = FTUDPPARSE(host, port)
    FTUDP.get_lidar_info_live()
    FTUDP.abandon_udp_data_in_cache()

    data, addr = FTUDP.udpsock.recvfrom(int(FTUDP.data_size) + 42)
    tail_dict = FTUDP.parse_FT_tail(data)
    csv_header = list(tail_dict.keys())
    savedir = os.path.join(save_path, r'tail_data_{}.csv'.format(datetime.now().strftime("%Y%m%d%H%M")))
    write_csv_header(csv_header, savedir)

    udp_num = time_sec * 1600
    _stopsignal = object()

    def producer(loops, out_q):
        for _ in range(loops):
            data, addr = FTUDP.udpsock.recvfrom(int(FTUDP.data_size) + 42)
            out_q.put(data)
        out_q.put(_stopsignal)

    def consumer(in_q):
        csv_rows = []
        while True:
            data = in_q.get()
            if data is _stopsignal:
                in_q.put(_stopsignal)
                break
            tail_dict = FTUDP.parse_FT_tail(data)
            tail_value_list = list(tail_dict.values())
            csv_rows.append(tail_value_list)
            if len(csv_rows) % 1600 == 0:
                write_n_row_to_csv(csv_rows, savedir)
                csv_rows = []

    q = Queue()
    t1 = Thread(target=consumer, args=(q,))
    t2 = Thread(target=producer, args=(udp_num, q))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print('test done!')









def udp_tail_sycn_angle_live(udp_num, save_path, spad_shift, rx_shift, host='', port=51233):
    FTUDP = FTUDPPARSE(host, port)
    FTUDP.get_lidar_info_live()
    FTUDP.abandon_udp_data_in_cache()
    data, addr = FTUDP.udpsock.recvfrom(int(FTUDP.data_size) + 42)
    tail_dict = FTUDP.parse_FT_tail(data)
    csv_header = list(tail_dict.keys()) + ['tx_angle', 'sync_angle']
    savedir = os.path.join(save_path, r'tail_data_{}.csv'.format(datetime.now().strftime("%Y%m%d%H%M")))
    write_csv_header(csv_header, savedir)
    csv_rows = []
    datas = []
    FTUDP.abandon_udp_data_in_cache()

    ft_angle_list = defaultdict(list)
    angle_list = []
    for i in range(54):
        column_id = []
        for j in range(max(0, i * 3 + spad_shift - rx_shift), min(160, (i + 1) * 3 + spad_shift - rx_shift)):
            column_id.append(j)
        angle = np.mean(
            (ft_ideal_angle_list[max(0, i * 3 + spad_shift - rx_shift): min(160, (i + 1) * 3 + spad_shift - rx_shift)]))
        ft_angle_list['tx{}'.format(i)].append(column_id)
        ft_angle_list['tx{}'.format(i)].append(angle)
        angle_list.append(angle)

    for _ in range(udp_num):
        data, addr = FTUDP.udpsock.recvfrom(int(FTUDP.data_size) + 42)
        datas.append(data)
    for data in datas:
        tail_dict = FTUDP.parse_FT_tail(data)
        for txidx in ft_angle_list.keys():
            if tail_dict['Column_ID'] in ft_angle_list[txidx][0]:
                tx_angle = ft_angle_list[txidx][1]
                chosen_idx = int(txidx[2: ])

        timestamp = tail_dict['Timestamp'] % 100000

        for idx, value in enumerate(ft_10hz_time_list):
            if value * 1000 >= timestamp:
                syncidx = (chosen_idx - idx + 53) % 53
                sync_anlge = angle_list[syncidx]
                break

        tail_value_list = list(tail_dict.values()) + [tx_angle, sync_anlge]
        csv_rows.append(tail_value_list)
    write_n_row_to_csv(csv_rows, savedir)


def pcap_tail2csv(pcap_file, savepath):
    FT = FTUDPPARSE()
    FT.get_lidar_info_from_pcap(pcap_file)
    savedir = os.path.join(savepath, r'pacp_tail_{}.csv'.format(datetime.now().strftime("%Y%m%d%H%M")))
    tail_dict = FT.parse_FT_tail(FT.first_data)
    csv_header = list(tail_dict)
    write_csv_header(csv_header, savedir)
    csv_rows = []
    with open(pcap_file, 'rb') as file_handle:
        for data_type, data, point_flag in FT.pcap_data_to_generator(file_handle):
            if point_flag:
                tail_dict = FT.parse_FT_tail(data)
                tail_value_list = list(tail_dict.values())
                csv_rows.append(tail_value_list)
            else:
                pass
    write_n_row_to_csv(csv_rows, savedir)



def udp_body_live(udp_num, body_type, save_path, host='', port=2368):
    FTUDP = FTUDPPARSE(host, port)
    FTUDP.get_lidar_info_live()
    FTUDP.abandon_udp_data_in_cache()
    savedir = os.path.join(save_path, r'body_{}_{}.csv'.format(body_type, datetime.now().strftime("%Y%m%d%H%M")))
    csv_header = ['Column_ID'] + [str(i + 1) for i in range(FTUDP.channel_num)]
    write_csv_header(csv_header, savedir)
    csv_rows = []
    datas = []
    for _ in range(udp_num):
        data, addr = FTUDP.udpsock.recvfrom(int(FTUDP.data_size) + 42)
        datas.append(data)
    for data in datas:
        tail_dict = FTUDP.parse_FT_tail(data)
        body_dict = FTUDP.parse_FT_body(data)
        row = [tail_dict['Column_ID']] + body_dict[body_type]
        csv_rows.append(row)
    write_n_row_to_csv(csv_rows, savedir)


def pcap_body2csv(pcap_file, body_type, savepath):
    FT = FTUDPPARSE()
    FT.get_lidar_info_from_pcap(pcap_file)
    savedir = os.path.join(savepath, r'pcap_body_{}_{}.csv'.format(body_type, datetime.now().strftime("%Y%m%d%H%M")))
    csv_header = ['Column_id'] + [str(i + 1) for i in range(FT.channel_num)]
    write_csv_header(csv_header, savedir)
    csv_rows = []
    with open(pcap_file, 'rb') as file_handle:
        for data_type, data, point_flag in FT.pcap_data_to_generator(file_handle):
            if point_flag:
                tail_dict = FT.parse_FT_tail(data)
                body_dict = FT.parse_FT_body(data)
                row = [tail_dict['Column_ID']] + body_dict[body_type]
                csv_rows.append(row)
            else:
                pass
    write_n_row_to_csv(csv_rows, savedir)


def write_csv_header(header, savefile):
    with open(savefile, 'w', encoding='utf8', newline='') as csvfile:
        myWrite = csv.writer(csvfile)
        myWrite.writerow(header)


def write_one_row_to_csv(csv_row, savefile):
    with open(savefile, 'a+', encoding="utf8", newline="") as csvfile:
        myWriter = csv.writer(csvfile)
        myWriter.writerow(csv_row)


def write_n_row_to_csv(csv_rows, savefile):
    with open(savefile, 'a+', encoding='utf8', newline='') as csvfile:
        myWriter = csv.writer(csvfile)
        for csv_row in csv_rows:
            myWriter.writerow(csv_row)


if __name__ == "__main__":
    # ----------------------------雷达在线tail转csv-----------------------------------------------------------------------
    # func： 雷达在线tail转csv的函数; param: (udp包个数, 结果保存文件夹地址); return: csv文件; 适用于FT雷达
    # udp_tail_live(1600, r'D:\WORK\FT\时间戳规律')

    # ----------------------------雷达在线body距离转csv--------------------------------------------------------------------
    # func： 雷达在线Body转csv的函数
    # param1: 帧数
    # param2: 获取Body中数据的类型 dist / ref / background_light / conf
    # param3: 保存csv的目录
    # udp_body_live(16000, 'dist', r'/home/hesai/FT120_0425')

    # ----------------------------雷达离线tail转csv-----------------------------------------------------------------------
    # func: 雷达离线tail转csv的函数； param: (pcap文件地址，结果csv保存目录)
    pcap_tail2csv(r'C:\Users\wanghaibo\Downloads\FT120_-100us.pcap', r'D:\WORK\FT')

    # ----------------------------雷达离线body距离转csv--------------------------------------------------------------------
    # func： 雷达离线Body转csv的函数
    # param1: pcap包的路径
    # param2: 获取Body中数据的类型 dist / ref / background_light / conf
    # param3: 保存csv的目录
    # udp_body_live(1600, 'dist', r'D:\WORK\FT')
    # pcap_body2csv(r'D:\WORK\FT\point_cloud.pcap', 'conf', r'D:\WORK\FT')

    # udp_tail_sycn_angle_live(16000, r'/home/hesai/FT120', 3, 4)

    # ----------------------------多线程在线tail转csv(用于长跑)-------------------------------------------------------------
    # param: (时间s，结果csv保存目录)
    # udp_tail_live_long(20, r'/home/hesai/FT120')


    # #
    # FT = FTUDPPARSE(network_card='')
    # FT.get_lidar_info_live()
    # datas = []
    # FT.abandon_udp_data_in_cache()
    # for _ in range(35):
    #     data, _ = FT.udpsock.recvfrom(int(FT.data_size) + 42)
    #     tail_dict = FT.parse_FT_tail(data)
    #     print(tail_dict)




    # from LidarDriverTotal import LidarDriver
    # ld = LidarDriver(lidar_full_type='FT120C1X', init_udp=False)
    # res = ld.ptc.set_ptc_sub_fpga2_para('/home/hesai/Downloads/C_FT38CA519338CA51_1.00.34p_c8246396_refcalib.param')
    # print('=====res:{}'.format(res))