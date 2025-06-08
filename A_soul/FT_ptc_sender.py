# -*- coding: UTF-8 -*-
import os.path
import socket
import time
import struct
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from datetime import datetime
import math


class PTC_CMD:
    def __init__(self, host='192.168.1.201', ptc_port=9347, network_card=''):
        self.host = host
        self.ptc_port = ptc_port
        self.network_card = network_card

    def ptc_sender(self, raw_cmd_code, payload, timeout=60):  # raw_cmd_code：整数(10进制or16进制)  payload：字节流
        """
        :param cmd_code: should be like 23 or 0x17
        :param payload: bytes
        :return:
        """
        self.ptc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.network_card != '':
            try:
                self.ptc_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, self.network_card.encode('utf-8'))
                print('已绑定网卡：{}'.format(self.network_card))
            except Exception as e:
                print('绑定网卡失败：{}'.format(self.network_card))
                input('继续吗？')

        self.ptc_socket.connect((self.host, self.ptc_port))
        self.ptc_socket.settimeout(timeout)

        cmd_code = struct.pack('>B', raw_cmd_code)
        if not payload or payload.upper() == "NONE":
            data = b'\x47\x74' + cmd_code + b'\x00\x00\x00\x00\x00'
        else:
            payload_len = len(payload)
            data = b'\x47\x74' + cmd_code + b'\x00' + struct.pack('>L', payload_len) + payload
        try:
            self.ptc_socket.send(data)
        except socket.timeout as e1:
            print('ptc SEND timeout: command 0x{:02x} with {}'.format(raw_cmd_code, e1))
            return {'send_timeout': 1}
        try:
            response = self.ptc_socket.recv(8)
            # print(response.hex())
        except socket.timeout as e1:
            print('ptc RECV_1 timeout: command 0x{:02x} with {}'.format(raw_cmd_code, e1))
            return {'recv_timeout': 1}
        else:
            r_cmd = int.from_bytes(response[2:3], 'big')
            r_returnCode = int.from_bytes(response[3:4], 'big')
            r_length = int.from_bytes(response[4:8], 'big')
            if r_length:
                try:
                    response_payload = b''
                    while len(response_payload) < r_length:
                        response_payload += self.ptc_socket.recv(r_length)
                except socket.timeout as e1:
                    print('ptc RECV_2 timeout: command 0x{:02x} with {}'.format(raw_cmd_code, e1))
                    return {'recv_timeout': 1}
            else:
                response_payload = ''

            final_response = {
                "response_command": r_cmd,
                "response_return_code": r_returnCode,
                "response_payload_length": r_length,
                "response_payload": response_payload
            }
            self.ptc_socket.close()
            time.sleep(1)
            return final_response

    def ptc_command_get_lidar_calibration_a2(self):
        cmd = 0x05
        payload = 'None'
        try:
            final_response = self.ptc_sender(cmd, payload)
            r_srting = final_response['response_payload'].decode()
            rows = r_srting.split('\r\n')
            with open('calibration.csv', 'w+', encoding='utf8', newline='') as csvfile:
                myWriter = csv.writer(csvfile)
                for csv_row in rows:
                    row = csv_row.split(',')
                    myWriter.writerow(row)

            df = pd.read_csv('calibration.csv', index_col=None, header=1)
            df = df.drop(index=[len(df)-1]).reset_index(drop=True)
            df[['Column_id']] = df[['Column_id']].astype(int)
            return df
        except Exception as e:
            print('An exception happened: '.format(str(e)))
            return 0

    def ptc_command_get_lidar_calibration_a3(self, savepath=''):
        tic = time.time()
        cmd = 0x05
        payload = 'None'
        final_response = self.ptc_sender(cmd, payload)
        # print(final_response)
        status = final_response['response_return_code']
        print(status)
        re_payload = final_response['response_payload']
        print(len(re_payload))
        # print(re_payload)
        # 角度文件存为dat文件
        if savepath != '':
            # pass
            save_dir = os.path.join(savepath, 'calibration.dat')
        else:
            save_dir = 'calibration.dat'

        with open(save_dir, 'wb') as file_handle:
            file_handle.write(re_payload)

        # 读取本地角度文件dat，返回1、水平角度160*120的ndarray, 2、垂直角度160*120的ndarray, 3、角度文件DataFrame
        ft_a3_calibration_21 = np.dtype([
            ('eeff', 'S2'),
            ('protocol_version_major', 'u1'),
            ('protocol_version_minor', 'u1'),
            ('reserved', 'u2'),
            ('column_number', 'u1'),
            ('channel_number', 'u1'),
            ('resolution', 'u1'),
            ('azimuth_adjust', 'i4', 160 * 120),
            ('elevation_adjust', 'i4', 160 * 120),
            ('sha_256_value', 'u1', 32)
        ])
        with open('calibration.dat', 'rb') as file_handle1:
            data = file_handle1.read()
        calib_data = np.frombuffer(data, dtype=ft_a3_calibration_21)
        # print(len(data))
        angle_resolution = calib_data['resolution'][0]
        azimuth_adjust = (calib_data['azimuth_adjust'][0] * 0.01).reshape((160, 120))
        elevation_adjust = (calib_data['elevation_adjust'][0] * 0.01).reshape((160, 120))

        # 转ndarray为DataFrame
        angle_dtype = [
            ('channel', 'u1'),
            ('column_id', 'u1'),
            ('elevation', 'float64'),
            ('azimuth', 'float64'),
        ]
        angle_data = np.zeros(160 * 120, dtype=angle_dtype)
        angle_data['channel'] = np.tile(np.arange(1, 121), 160)
        angle_data['column_id'] = np.repeat(np.arange(0, 160), 120)
        angle_data['elevation'] = calib_data['elevation_adjust'][0] * 0.01
        angle_data['azimuth'] = calib_data['azimuth_adjust'][0] * 0.01
        df_correction = pd.DataFrame(angle_data)
        df_correction.columns = ['Channel', 'Column_id', 'Elevation', 'Azimuth']
        print(df_correction)
        toc = time.time()
        print('Time Consuming: {}'.format(toc - tic))
        return azimuth_adjust, elevation_adjust, df_correction


    def ptc_command_get_lidar_calibration_a3_slice(self):
        tic = time.time()
        cmd = 0x05
        payload = 'None'
        ptc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ptc_socket.connect((self.host, 9347))
        ptc_socket.settimeout(600)
        cmd_code = struct.pack('>B', cmd)
        send_data = b'\x47\x74' + cmd_code + b'\x00\x00\x00\x00\x00'
        try:
            ptc_socket.send(send_data)
            return_message = ptc_socket.recv(8)
            re_payload_length = int.from_bytes(return_message[4: 8], byteorder='big')

            print('Return message length: {}'.format(re_payload_length))
            re_payload = b''
            while re_payload_length > 0:
                data = ptc_socket.recv(1024)
                # print(len(data), data)
                re_payload += data
                re_payload_length -= 1024

            print('receive done: length is {}'.format(len(re_payload)))
            # 角度文件存为dat文件
            with open('calibration.dat', 'wb') as file_handle:
                file_handle.write(re_payload)

            # 读取本地角度文件dat，返回1、水平角度160*120的ndarray, 2、垂直角度160*120的ndarray, 3、角度文件DataFrame
            ft_a3_calibration_21 = np.dtype([
                ('eeff', 'S2'),
                ('protocol_version_major', 'u1'),
                ('protocol_version_minor', 'u1'),
                ('reserved', 'u2'),
                ('column_number', 'u1'),
                ('channel_number', 'u1'),
                ('resolution', 'u1'),
                ('azimuth_adjust', 'i4', 160 * 120),
                ('elevation_adjust', 'i4', 160 * 120),
                ('sha_256_value', 'u1', 32)
            ])
            with open('calibration.dat', 'rb') as file_handle1:
                data = file_handle1.read()
            calib_data = np.frombuffer(data, dtype=ft_a3_calibration_21)
            print(len(data))
            angle_resolution = calib_data['resolution'][0]
            azimuth_adjust = (calib_data['azimuth_adjust'][0] * 0.01).reshape((160, 120))
            elevation_adjust = (calib_data['elevation_adjust'][0] * 0.01).reshape((160, 120))

            # 转ndarray为DataFrame
            angle_dtype = [
                ('channel', 'u1'),
                ('column_id', 'u1'),
                ('elevation', 'float64'),
                ('azimuth', 'float64'),
            ]
            angle_data = np.zeros(160 * 120, dtype=angle_dtype)
            angle_data['channel'] = np.tile(np.arange(1, 121), 160)
            angle_data['column_id'] = np.repeat(np.arange(0, 160), 120)
            angle_data['elevation'] = calib_data['elevation_adjust'][0] * 0.01
            angle_data['azimuth'] = calib_data['azimuth_adjust'][0] * 0.01
            df_correction = pd.DataFrame(angle_data)
            df_correction.columns = ['Channel', 'Column_id', 'Elevation', 'Azimuth']
            print(df_correction)
            toc = time.time()
            print('Time Consuming: {}'.format(toc - tic))
            return azimuth_adjust, elevation_adjust, df_correction

        except Exception as e:
            print('An exception happened: '.format(str(e)))
            return 0

    def ptc_command_get_inventory_info_1(self):
        cmd = 0x07
        payload = 'None'
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)
        info_name = ['sn', 'pn', 'data_of_manufacture', 'mac', 'sw_ver', 'hw_ver', 'control_fw_ver', 'sensor_fw_ver',
                     'fpga_para_ver', 'fpga_cfg_ver', 'fpga_para_sha', 'fpga_cfg_sha', 'angle_offset',
                     'model_code_production', 'model_code', 'num_of_lines', 'motor_correction_flag',
                     'codewheel_correction_flag', 'motor_type']
        info_type = ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 'int', 'int', 'int', 'int', 'int',
                     'int', 'int']
        re_payload = final_response['response_payload']
        # print(len(re_payload))
        print('MAC', re_payload[66: 72].hex())
        res = struct.unpack('>18s32s16s6s16s16s16s16s16s16s16s16shBBHBBB47s', re_payload)
        # print(res)
        enum_dict = {
            'model_code': {0: 'Pandar40P', 2: 'Pandar64', 3: 'Pandar128', 15: 'PandarQT', 17: 'Pandar40M',
                           42: 'PandarOT'},
            'motor_type': {0: 'single_direction', 1: 'dual_direction'}
        }
        result_dic = {}
        for i, name in enumerate(info_name):
            res_value = res[i]
            if info_type[i] == 's':
                try:
                    res_info = res_value.decode().strip().strip(b'\x00'.decode())
                    print(name, len(res[i]), res[i], res[i].hex())
                except:
                    res_info = res_value.hex()  # TODO 待确认后更改
            else:
                res_info = res[i]
                # print(name, res[i], hex(res[i]))
            result_dic.update({name: res_info})
        print(result_dic)
        return result_dic

    def ptc_command_get_inventory_info_A3V2(self):
        cmd = 0x07
        payload = 'None'
        final_response = self.ptc_sender(cmd, payload)
        re_payload = final_response['response_payload']
        result_dic = {}
        result_dic['sn'] = re_payload[0: 18].decode().strip().strip(b'\x00'.decode())
        result_dic['pn'] = re_payload[18: 50].decode().strip().strip(b'\x00'.decode())
        result_dic['data_of_manufacture'] = re_payload[50: 66].decode().strip().strip(b'\x00'.decode())
        result_dic['mac'] =  re_payload[66: 72].hex()
        result_dic['sw_ver'] = re_payload[72: 88].decode().strip().strip(b'\x00'.decode())
        result_dic['hw_ver'] = re_payload[88: 104].decode().strip().strip(b'\x00'.decode())
        result_dic['control_fw_ver (fpga bit)'] = re_payload[104: 120].decode().strip().strip(b'\x00'.decode())
        result_dic['sensor_fw_ver (fpga sha)'] = re_payload[120: 136].decode().strip().strip(b'\x00'.decode())
        result_dic['fpga_para_ver (fpga para2)'] = re_payload[136: 152].decode().strip().strip(b'\x00'.decode())
        result_dic['fpga_cfg_ver (fpga para1)'] = re_payload[152: 168].decode().strip().strip(b'\x00'.decode())
        result_dic['fpga_para_sha'] = re_payload[168: 184].decode().strip().strip(b'\x00'.decode())
        result_dic['fpga_cfg_sha'] = re_payload[184: 200].decode().strip().strip(b'\x00'.decode())
        result_dic['angle_offset'] = int.from_bytes(re_payload[200: 202], 'big')
        result_dic['model_code'] = int.from_bytes(re_payload[202: 204], 'big')
        result_dic['num_of_lines'] = int.from_bytes(re_payload[204: 206], 'big')
        result_dic['motor_correction_flag'] = {0: 'motor correction unfinished', 1: 'motor correction finished'}[re_payload[206]]
        result_dic['codewheel_correction_flag'] = {0: 'codewheel_correction unfinished', 1: 'codewheel_correction finished'}[re_payload[207]]
        result_dic['motor_type'] = {0: 'single direction', 1: 'dual direction'}[re_payload[208]]

    def ptc_command_get_inventory_info_A3V3(self):
        cmd = 0x07
        payload = 'None'
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)
        re_payload = final_response['response_payload']
        # print('re_Payload length: {}'.format(len(re_payload)))
        result_dic = {}
        result_dic['sn'] = re_payload[0: 18].decode().strip().strip(b'\00'.decode())
        result_dic['pn'] = re_payload[18: 50].decode().strip().strip(b'\00'.decode())
        result_dic['data_of_manufacture'] = re_payload[50: 66].decode().strip().strip(b'\00'.decode())
        result_dic['mac'] = ':'.join(['{:02x}'.format(i).upper() for i in re_payload[66: 72]])
        result_dic['sw_ver'] = re_payload[72: 88].decode().strip().strip(b'\00'.decode())
        result_dic['hw_ver (Not Supported)'] = re_payload[88: 104].decode().strip().strip(b'\00'.decode())
        result_dic['control_fw_ver (fpga bit)'] = re_payload[104: 120].decode().strip().strip(b'\x00'.decode())
        # result_dic['sensor_fw_ver (fpga sha)'] = re_payload[120: 136].decode().strip().strip(b'\x00'.decode())
        result_dic['sensor_fw_ver (fpga sha)'] = ''.join(['{:02x}'.format(i) for i in re_payload[120: 124]])
        result_dic['fpga_para_ver (fpga para2)'] = re_payload[136: 152].decode().strip().strip(b'\x00'.decode())
        result_dic['fpga_cfg_ver (fpga para1)'] = re_payload[152: 168].decode().strip().strip(b'\x00'.decode())
        result_dic['fpga_para_sha'] = re_payload[168: 184].decode().strip().strip(b'\x00'.decode())
        result_dic['fpga_cfg_sha'] = re_payload[184: 200].decode().strip().strip(b'\x00'.decode())
        result_dic['angle_offset (not supported)'] = int.from_bytes(re_payload[200: 202], 'big')
        result_dic['model_code'] = re_payload[202]
        result_dic['motor_type (not supported)'] = re_payload[203]
        result_dic['num_of_lines'] = re_payload[204]
        result_dic['motor_correction_flag'] = re_payload[205]
        result_dic['codewheel_correction_flag'] = re_payload[206]
        print(result_dic)
        return result_dic

    def ptc_command_ptp_diagnostics(self, ptp_query_type):
        cmd = 0x06
        payload = {'PTP STATUS': 1,
                   'PTP TLV PORT_DATA_SET': 2,
                   'PTP TLV TIME_STATUS_NP': 3}[ptp_query_type.upper()].to_bytes(1, 'big')
        final_response = self.ptc_sender(cmd, payload)
        re_payload = final_response['response_payload']
        master_offset = int.from_bytes(re_payload[: 8], 'big', signed=True)
        average_offset = int.from_bytes(re_payload[8: 16], 'big', signed=True)
        ptp_state = {0: 'NONE',
                     1: 'INITIALIZING',
                     2: 'FAULTY',
                     3: 'DISABLED',
                     4: 'LISTENING',
                     5: 'PRE_MASTER',
                     6: 'MASTER',
                     7: 'PASSIVE',
                     8: 'UNCALIBRATED',
                     9: 'SLAVE',
                     10: 'GRAND_MASTER'}[int.from_bytes(re_payload[16: 20], 'big')]
        elapsed_millisec = int.from_bytes(re_payload[20: 24], 'big')
        print('master_offset: {}\n'
              'average_master_offset: {}\n'
              'ptp_state: {}\n'
              'elapsed_millisec: {}'.format(master_offset, average_offset, ptp_state,elapsed_millisec))

    def ptc_command_get_config_info_1(self):
        cmd = 0x08
        payload = 'None'
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)
        info_name = ['ipaddr', 'mask', 'gateway', 'dest_ipaddr', 'dest_ptcloud_udp_port', 'dest_gps_udp_port',
                     'spin_rate', 'sync', 'sync_angle', 'start_angle', 'stop_angle', 'clock_source', 'udp_seq',
                     'trigger_method', 'return_mode', 'standby_mode', 'motor_status', 'vlan_flag', 'vlan_id',
                     'clock_data_fmt', 'noise_filtering', 'reflectivity_mapping']
        info_idx = [4, 4, 4, 4, 2, 2, 2, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1]
        re_payload = final_response['response_payload']
        print(re_payload[16: 18].hex())
        res = struct.unpack('>16BHHHBHHH7BH3B', re_payload[:-23])
        result_dic = {}
        for i, message in enumerate(info_name):
            info_value = res[i]
            if i < 4:
                info_value = '.'.join([str(i) for i in res[sum(info_idx[: i]): sum(info_idx[: i+1])]])
            result_dic.update({message: info_value})
        print(result_dic)

    def ptc_command_get_config_info(self):
        cmd = 0x08
        payload = 'None'
        final_response = self.ptc_sender(cmd, payload)
        # print(final_response)
        re_payload = final_response['response_payload']
        print(len(re_payload))
        print(re_payload.hex())
        result = {}
        ips = struct.unpack('>4B', re_payload[0: 4])
        ip = '.'.join([str(i) for i in ips])
        result['ipaddr'] = ip

        masks = struct.unpack('>4B', re_payload[4: 8])
        mask = '.'.join([str(i) for i in masks])
        result['mask'] = mask

        gateways = struct.unpack('>4B', re_payload[8: 12])
        gateway = '.'.join([str(i) for i in gateways])
        result['gateway'] = gateway

        dest_ipaddrs = struct.unpack('>4B', re_payload[12: 16])
        dest_ipaddr = '.'.join([str(i) for i in dest_ipaddrs])
        result['dest_ipaddr'] = dest_ipaddr

        result['dest_udp_port'] = int.from_bytes(re_payload[16: 18], 'big')
        result['dest_gps_port'] = int.from_bytes(re_payload[18: 20], 'big')
        result['spin_rate'] = int.from_bytes(re_payload[20: 22], 'big')
        result['sync_enable'] = {0: 'Disable', 1: 'Enable'}[re_payload[22]]
        result['sync_angle'] = int.from_bytes(re_payload[23: 25], 'big')
        result['return_mode'] = {1: 'Strongest Return', 3: 'First Return', 5:'First and Strongest Return'}[re_payload[32]]
        result['standby_mode'] = {0: 'in operation', 1: 'standby'}[re_payload[33]]
        print(result)
        return result

    def ptc_command_get_lidar_status(self):
        cmd = 0x09
        payload = 'None'
        final_response = self.ptc_sender(cmd, payload)
        re_payload = final_response['response_payload']
        print('re_payload length: {}'.format(len(re_payload)))
        system_uptime = int.from_bytes(re_payload[0: 4], 'big')
        startup_times = int.from_bytes(re_payload[44: 48], 'big')
        total_operation_time = int.from_bytes(re_payload[48: 52], 'big')
        ptp_clock_status = {0: 'free tun', 1: 'tracking', 2: 'locked', 3: 'frozen'}[re_payload[52]]
        humidity = int.from_bytes(re_payload[53: 57], 'big')
        print('System Uptime: {}s\n'
              'Startup Times: {}\n'
              'Total Operartion Time: {}\n'
              'PTP Clock Status: {}.\n'
              'Humidity: {} (Not used).'.format(system_uptime, startup_times, total_operation_time, ptp_clock_status, humidity))
        return startup_times

    def ptc_command_get_register(self):  # TODO
        cmd = 0x0C
        payload = 'address here'
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)

    def ptc_command_reboot(self):
        cmd = 0x10
        payload = 'None'
        final_response = self.ptc_sender(cmd, payload)
        re_code = final_response['response_return_code']
        print(final_response)
        if re_code == 0:
            return 1
        else:
            return 0

    def ptc_command_standby_mode(self, mode='In operation'):
        cmd = 0x1c
        standby_mode_int = {'IN OPERATION': 0, 'STANDBY': 1}[mode.upper()]
        payload = struct.pack('>B', standby_mode_int)
        try:
            final_response = self.ptc_sender(cmd, payload)
            print(final_response)
            if final_response['response_return_code'] == 0:
                print('Set mode to {:s} successfully.'.format(mode))
        except Exception as e:
            print("An exception happened: " + str(e))

    def ptc_command_set_return_mode(self, return_mode='first return'):
        cmd = 0x1e
        return_mode_int = {'STRONGEST RETURN': 1, 'FIRST RETURN': 3, 'FIRST AND STRONGEST RETURN': 5}[
            return_mode.upper()]
        payload = struct.pack('>B', return_mode_int)
        print(payload.hex())
        try:
            final_response = self.ptc_sender(cmd, payload)
            print(final_response)
            if final_response['response_return_code'] == 0:
                print('Set mode to {:s} successfully.'.format(return_mode))
        except Exception as e:
            print("An exception happened: " + str(e))

    def ptc_command_set_destination_ip(self, des_ip, port, gps_port, des_mac, src_ip, src_port, src_mac):
        cmd = 0x20
        payload = b''
        for i in des_ip.split('.'):
            payload += struct.pack('>B', int(i))
        payload += struct.pack('>HH', port, gps_port)
        for i in des_mac.split(':'):
            payload += bytes.fromhex(i)
        for i in src_ip.split('.'):
            payload += struct.pack('>B', int(i))
        payload += struct.pack('>H', src_port)
        for i in src_mac.split(':'):
            payload += bytes.fromhex(i)
        print(len(payload), payload.hex())
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)

    def ptc_command_set_control_port(self, ip, mask, gateway, vlan_flag, vlan_id, port):
        cmd = 0x21
        payload = b''
        for i in ip.split('.'):
            payload += struct.pack('>B', int(i))
        for i in mask.split('.'):
            payload += struct.pack('>B', int(i))
        for i in gateway.split('.'):
            payload += struct.pack('>B', int(i))
        vlan_flag_int = {'OFF': 0, 'ON': 1}[vlan_flag.upper()]
        payload += struct.pack('>BHH', vlan_flag_int, vlan_id, port)
        print(len(payload), payload.hex())
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)

    def ptc_command_get_freeze_frame_info(self):
        cmd = 0xA1
        payload = b'\x02'
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)
        re_payload = final_response['response_payload']
        if len(re_payload) == 0:
            return 0, []
        else:
            fault_code_list = []
            re_dict = {}
            for i in range(int(len(re_payload) / 267)):
                re_dict['frame_{}'.format(i)] = re_payload[267 * i: 267 * (i + 1)].hex()
                str_code = re_payload[267 * i + 1: 267 * i + 2].hex() + re_payload[267 * i: 267 * i + 1].hex()
                fault_code_list.append(str_code)
            return re_dict, fault_code_list

    def ptc_command_clear_ff(self):
        cmd = 0xA1
        payload = b'\x04'
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)

    def ptc_sub_command_get_adc(self, fac_flag):
        cmd = 0xff
        fac_flag_byte = {'FAC': b'\x01', 'RELEASE': b'\x00'}[fac_flag.upper()]
        payload = b'\x00' + fac_flag_byte + b'\x00\x15'
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)
        re_payload = final_response['response_payload']
        pwrin_vol = int.from_bytes(re_payload[4: 8], 'big') / (2 ** 9)
        vout_hvcu = int.from_bytes(re_payload[8: 12], 'big') / (2 ** 9)
        mpb_ntc = int.from_bytes(re_payload[12: 16], 'big', signed=True) / (2 ** 7)
        trx_ntc = int.from_bytes(re_payload[16: ], 'big', signed=True) / (2 ** 7)
        print('Power in vol: {}\n'
              'Vout HVcu: {}\n'
              'mpb_ntc: {}\n'
              'trx_ntc: {}'.format(pwrin_vol, vout_hvcu, mpb_ntc, trx_ntc))
        return pwrin_vol, pwrin_vol, mpb_ntc, trx_ntc

    def ptc_command_set_freeze_frame_clear(self):
        cmd = 0x31
        payload = 'None'
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)

    def ptc_command_set_sleep(self):
        cmd = 0xab


    def ptc_command_set_ptp_config(self, ptp_status, profile, domain, network, tsn_switch):
        cmd = 0x24
        ptp_status_bytes = {'DISABLE': 0, 'ENABLE': 1}[ptp_status.upper()].to_bytes(1, 'big')
        profile_bytes = {'802.1AS-autosar': 3, '802.1AS-automotive': 2}[profile].to_bytes(1, 'big')
        domain_bytes = domain.to_bytes(1, 'big')
        network_bytes = {'UDP/IP': 0, 'L2': 1}[network.upper()].to_bytes(1, 'big')
        tsn_switch_bytes = {'NON-TSN': 0, 'TSN': 1}[tsn_switch.upper()].to_bytes(1, 'big')
        payload = ptp_status_bytes + profile_bytes + domain_bytes + network_bytes+ tsn_switch_bytes
        print(payload)
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)

    def ptc_command_get_ptp_config(self):
        cmd = 0x26
        payload = 'None'
        final_response = self.ptc_sender(cmd, payload)
        re_response = final_response['response_payload']
        print(final_response)
        status = {0: 'Disable', 1: 'Enable'}[re_response[0]]
        profile = {3: '802.1AS Autosar', 2:'802.1AS-automotive'}[re_response[1]]
        domain = re_response[2]
        network = {0: 'UDP/IP', 1: 'L2'}[re_response[3]]
        tsn_switch = {0: 'Non-TSN', 1: 'TSN'}[re_response[4]]
        print('gPTP status: {}\n'
              'Profile: {}\n'
              'Domain: {}\n'
              'Network: {}\n'
              'TSN-switch: {}'.format(status, profile, domain, network, tsn_switch))
        re_payload_str = re_response.hex()
        return re_payload_str

    def ptc_command_get_mode_fault_info(self):
        cmd = 0x8d
        payload = 'None'
        final_response = self.ptc_sender(cmd, payload)
        re_payload = final_response['response_payload']
        work_mode = {0: 'Energy-Saving',
                     1: 'Standard',
                     2: 'Standby',
                     3: 'High-Temp-Shutdown',
                     4: 'Shutdown'}[re_payload[0]]
        energy_saving_fault = {0: 'No Energy-Saving fault',
                               1: 'Energy-saving fault exsits'}[re_payload[1] & 0b1111]
        high_temp_shutdown_fault = {0: 'No High-Temp-Shutdown fault',
                                    1: 'High-Temp-Shutdown fault exists'}[(re_payload[1] >> 4) & 0b1]
        other_shutdown_fault = 'No Other-Shutdown fault' if not (re_payload[1] >> 5) & 0b111 else 'Other-Shutdown fault exists'

        print('Lidar work mode: {} \n'
              '{}\n'
              '{}\n'
              '{}'.format(work_mode, energy_saving_fault, high_temp_shutdown_fault, other_shutdown_fault))



    def ptc_sub_command_shutdown_protection(self, fac_flag):
        cmd = 0xff
        fac_flag_byte = {'FAC': b'\x01', 'RELEASE': b'\x00'}[fac_flag.upper()]
        payload = b'\x00' + fac_flag_byte + b'\x00\x28'
        print(payload.hex())
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)

    def ptc_sub_command_set_sn(self, fac_flag, sn):
        cmd = 0xff
        fac_flag_byte = {'FAC': b'\x01', 'RELEASE': b'\x00'}[fac_flag.upper()]
        payload = b'\x00' + fac_flag_byte + b'\x00\x01'
        sn_bytes = sn.encode('utf-8')
        while len(sn_bytes) < 18:
            sn_bytes += b'\x00'
        # print(sn_bytes, sn_bytes.hex(), len(sn_bytes))
        payload += sn_bytes
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)

    def ptc_sub_command_set_pn(self, fac_flag, pn):
        cmd = 0xff
        fac_flag_byte = {'FAC': b'\x01', 'RELEASE': b'\x00'}[fac_flag.upper()]
        payload = b'\x00' + fac_flag_byte + b'\x00\x03'
        pn_bytes = pn.encode('utf-8')
        while len(pn_bytes) < 32:
            pn_bytes += b'\x00'
        payload += pn_bytes
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)

    def ptc_sub_command_control_watchdog(self, fac_flag, jam_time):
        cmd = 0xff
        fac_flag_byte = {'FAC': b'\x01', 'RELEASE': b'\x00'}[fac_flag.upper()]
        payload = b'\00' + fac_flag_byte + b'\x00\x26'
        flag = b'\xee'
        time = struct.pack('>I', jam_time)
        payload += flag
        payload += time
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)
        re_code = final_response['response_return_code']
        if re_code == 0:
            return 1
        else:
            return 0

    def ptc_sub_command_sleep_mode(self, fac_flag, delay):
        cmd = 0xff
        fac_flag_byte = {'FAC': b'\x01', 'RELEASE': b'\x00'}[fac_flag.upper()]
        payload = b'\00' + fac_flag_byte + b'\x00\x2a'
        mode = b'\x01'
        delay_byte = struct.pack('>I', delay)
        payload += mode
        payload += delay_byte
        print(payload.hex())
        final_response = self.ptc_sender(cmd, payload)
        re_payload = final_response['response_payload']
        print(re_payload.hex())
        print(final_response)



    def ptc_sub_command_set_mac_address(self, fac_flag, mac):
        cmd = 0xff
        fac_flag_byte = {'FAC': b'\x01', 'RELEASE': b'\x00'}[fac_flag.upper()]
        payload = b'\x00' + fac_flag_byte + b'\x00\x00'
        mac_list = mac.split(':')
        mac = ''.join(mac_list)
        # print(mac)
        mac_bytes = bytes.fromhex(mac)
        payload += mac_bytes
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)

    def ptc_sub_command_set_lidar_angle_cali(self, fac_flag, file_path):
        cmd = 0xff
        fac_flag_byte = {'FAC': b'\x01', 'RELEASE': b'\x00'}[fac_flag.upper()]
        payload = b'\x00' + fac_flag_byte + b'\x00\x0f'
        with open(file_path, 'rb') as file_handle1:
            data = file_handle1.read()
        print(len(data))
        payload += data
        print(len(payload))
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)

    def ptc_sub_command_set_frame_rate(self, fac_flag, frame_rate):
        cmd = 0xff
        fac_flag_byte = {'FAC': b'\x01', 'RELEASE': b'\x00'}[fac_flag.upper()]
        payload = b'\x00' + fac_flag_byte + b'\x00\x54'
        frame_rate_int = {10: 0, 20: 1}[frame_rate]
        frame_rate_byte = frame_rate_int.to_bytes(1, 'big')
        payload += frame_rate_byte
        print(payload.hex())
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)

    def ptc_command_set_sync_angle(self, sync_angle_flag, sync_angle_value):
        cmd = 0x18
        payload = b''
        sync_angle_flag_bytes = {'OFF': 0, 'ON': 1}[sync_angle_flag.upper()].to_bytes(1, 'big')
        sync_angle_value_bytes = sync_angle_value.to_bytes(2, 'big')
        payload += sync_angle_flag_bytes
        payload += sync_angle_value_bytes
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)

    def ptc_sub_command_set_customer_frame_rate(self, fac_flag, frame_rate):
        cmd = 0xff
        fac_flag_byte = {'FAC': b'\x01', 'RELEASE': b'\x00'}[fac_flag.upper()]
        payload = b'\x00' + fac_flag_byte + b'\x00\x58'
        frame_rate_int = {10: 0, 20: 1}[frame_rate]
        frame_rate_byte = frame_rate_int.to_bytes(1, 'big')
        payload += frame_rate_byte
        final_reponse = self.ptc_sender(cmd, payload)
        print(final_reponse)

    def ptc_sub_command_set_customer_return_mode(self, fac_flag, return_mode):
        cmd = 0xff
        fac_flag_byte = {'FAC': b'\x01', 'RELEASE': b'\x00'}[fac_flag.upper()]
        payload = b'\x00' + fac_flag_byte + b'\x00\x59'
        print(payload.hex())
        return_mode_int = {'STRONGEST RETURN': 1, 'FIRST RETURN': 3, 'FIRST AND STRONGEST RETURN': 5}[
            return_mode.upper()]
        return_mode_bytes = return_mode_int.to_bytes(1, 'big')
        payload += return_mode_bytes
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)

    def ptc_sub_command_get_lidar_position(self, fac_flag):
        cmd = 0xff
        fac_flag_byte = {'FAC': b'\x01', 'RELEASE': b'\x00'}[fac_flag.upper()]
        payload = b'\x00' + fac_flag_byte + b'\x00\x55'
        final_response = self.ptc_sender(cmd, payload)
        re_payload = final_response['response_payload']
        print(re_payload.hex())
        pos = {0: 'LEFT', 1: 'RIGHT'}[re_payload[4]]
        print('Current Lidar Position: {}'.format(pos))
        return pos

    def ptc_sub_command_set_lidar_position(self, fac_flag, position):
        cmd = 0xff
        fac_flag_byte = {'FAC': b'\x01', 'RELEASE': b'\x00'}[fac_flag.upper()]
        payload = b'\x00' + fac_flag_byte + b'\x00\x56'
        pos_int = {'LEFT': 0, 'RIGHT': 1}[position.upper()]
        pos_bytes = pos_int.to_bytes(1, 'big')
        payload += pos_bytes
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)

    def ptc_sub_command_get_frame_rate(self, fac_flag):
        cmd = 0xff
        fac_flag_byte = {'FAC': b'\x01', 'RELEASE': b'\x00'}[fac_flag.upper()]
        payload = b'\x00' + fac_flag_byte + b'\x00\x5a'
        print(payload)
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)
        re_payload = final_response['response_payload']
        print(re_payload.hex())
        frame_rate = {0: 10, 1: 20}[re_payload[4]]
        print('Frame_rate: {}'.format(frame_rate))
        return frame_rate

    def ptc_sub_command_get_mcu_debug_info(self, fac_flag):
        cmd = 0xff
        fac_flag_byte = {'FAC': b'\x01', 'RELEASE': b'\x00'}[fac_flag.upper()]
        payload = b'\x00' + fac_flag_byte + b'\x00\x57'
        final_response = self.ptc_sender(cmd, payload)
        re_payload = final_response['response_payload']
        print(re_payload)
        cali_result = {0: 'OK', 1: 'Not OK'}[re_payload[4]]
        dna_result = {0: 'OK', 1: 'Not OK'}[re_payload[4 + 1]]
        print('Cali_result: {}; DNA_result: {}'.format(cali_result, dna_result))

    def ptc_sub_command_clear_nvm_area(self, fac_flag):
        cmd = 0xff
        fac_flag_byte = {'FAC': b'\x01', 'RELEASE': b'\x00'}[fac_flag.upper()]
        payload = b'\x00' + fac_flag_byte + b'\x00\x5B'
        final_response = self.ptc_sender(cmd, payload)
        re_code = final_response['response_return_code']
        if not re_code:
            return 1
        else:
            return 0

    def ptc_sub_command_set_para(self, fac_flag, srcIP, srcPort, srcMac, destIP, destPort,
                                 destMac, netMask, gateway, vlan_flag, vlan_id):
        cmd = 0xff
        fac_flag_byte = {'FAC': b'\x01', 'RELEASE': b'\x00'}[fac_flag.upper()]
        payload = b'\x00' + fac_flag_byte + b'\x00\x40'
        modulename = b'\x00\x02'
        paraID = b'\x00\x03'
        srcIP_bytes = b''.join(int(i).to_bytes(1, 'big') for i in srcIP.split('.'))
        srcPort_bytes = srcPort.to_bytes(2, 'big')
        srcMac_bytes = bytes.fromhex(''.join(i for i in srcMac.split(':')))

        destIP_bytes = b''.join(int(i).to_bytes(1, 'big') for i in destIP.split('.'))
        destPort_bytes = destPort.to_bytes(2, 'big')
        destMac_bytes = bytes.fromhex(''.join(i for i in destMac.split(':')))

        netMask_bytes = b''.join(int(i).to_bytes(1, 'big') for i in netMask.split('.'))
        gateway_bytes = b''.join(int(i).to_bytes(1, 'big') for i in gateway.split('.'))

        vlan_flag_bytes = vlan_flag.to_bytes(1, 'big')
        vlan_id_bytes = vlan_id.to_bytes(2, 'big')

        payload += modulename + paraID + srcIP_bytes + srcPort_bytes + srcMac_bytes + destIP_bytes + destPort_bytes + \
                   destMac_bytes + netMask_bytes + gateway_bytes + vlan_flag_bytes + vlan_id_bytes
        print(len(payload), payload.hex())
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)

    def ptc_sub_command_set_customer_udp_para(self, fac_flag, srcIP, srcPort, srcMac, destIP, destPort, destMac,
                                              netMask, gateway, vlan_flag, vlan_id):

        cmd = 0xff
        fac_flag_byte = {'FAC': b'\x01', 'RELEASE': b'\x00'}[fac_flag.upper()]
        payload = b'\x00' + fac_flag_byte + b'\x00\x5c'
        srcIP_bytes = b''.join(int(i).to_bytes(1, 'big') for i in srcIP.split('.'))
        srcPort_bytes = srcPort.to_bytes(2, 'big')
        srcMac_bytes = bytes.fromhex(''.join(i for i in srcMac.split(':')))

        destIP_bytes = b''.join(int(i).to_bytes(1, 'big') for i in destIP.split('.'))
        destPort_bytes = destPort.to_bytes(2, 'big')
        destMac_bytes = bytes.fromhex(''.join(i for i in destMac.split(':')))

        netMask_bytes = b''.join(int(i).to_bytes(1, 'big') for i in netMask.split('.'))
        gateway_bytes = b''.join(int(i).to_bytes(1, 'big') for i in gateway.split('.'))

        vlan_flag_bytes = vlan_flag.to_bytes(1, 'big')
        vlan_id_bytes = vlan_id.to_bytes(2, 'big')
        payload += srcIP_bytes + srcPort_bytes + srcMac_bytes + destIP_bytes + destPort_bytes + destMac_bytes + \
                   netMask_bytes + gateway_bytes + vlan_flag_bytes + vlan_id_bytes
        print(len(payload), payload.hex())
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)

    def ptc_sub_command_get_para(self, fac_flag, modulename):
        cmd = 0xff
        fac_flag_byte = {'FAC': b'\x01', 'RELEASE': b'\x00'}[fac_flag.upper()]
        payload = b'\x00' + fac_flag_byte + b'\x00\x41'
        if modulename == 'UDP':
            payload += b'\x00\x02' + b'\x00\x00'
        else:
            payload += b'\x00\x02' + b'\x00\x03'
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)
        re_payload = final_response['response_payload']
        print(len(re_payload))
        if final_response['response_return_code'] == 0:
            source_ip = '.'.join(str(i) for i in re_payload[4: 8])
            source_port = int.from_bytes(re_payload[8: 10], 'big')
            source_MAC = ':'.join('{:02x}'.format(i).upper() for i in re_payload[10: 16])
            dest_ip = '.'.join(str(i) for i in re_payload[16: 20])
            dest_port = int.from_bytes(re_payload[20: 22], 'big')
            dest_MAC = ':'.join('{:02x}'.format(i).upper() for i in re_payload[22: 28])
            netmask = '.'.join(str(i) for i in re_payload[28: 32])
            gateway = '.'.join(str(i) for i in re_payload[32: 36])
            vlan_flag = re_payload[36]
            vlan_id = int.from_bytes(re_payload[37: 39], 'big')
            print('  source_ip: {}\n'
                  'source_port: {}\n'
                  ' source_MAC: {}\n'
                  '    dest_ip: {}\n'
                  '  dest_port: {}\n'
                  '   dest_MAC: {}\n'
                  '    netmask: {}\n'
                  '    gateway: {}\n'
                  '  vlan_flag: {}\n'
                  '    vlan_id: {}'.format(source_ip, source_port, source_MAC, dest_ip, dest_port, dest_MAC, netmask,
                                           gateway, vlan_flag, vlan_id))
        else:
            print('Error: response_return_code = {}'.format(re_payload['response_return_code']))

    def ptc_sub_command_set_clear_time_statistic(self, fac_flag):
        cmd = 0xff
        fac_flag_byte = {'FAC': b'\x01', 'RELEASE': b'\x00'}[fac_flag.upper()]
        payload = b'\x00' + fac_flag_byte + b'\x00\x09'
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)

    def get_lidar_monitor(self, fac_flag):
        cmd = 0xff
        fac_flag_byte = {'FAC': b'\x01', 'RELEASE': b'\00'}[fac_flag.upper()]
        payload = b'\x00' + fac_flag_byte + b'\x00\x15'
        final_reponse = self.ptc_sender(cmd, payload)
        print(final_reponse)
        re_payload = final_reponse['response_payload']
        input_valtage = int.from_bytes(re_payload[4: 8], byteorder='big', signed=False) * 0.01
        input_current = int.from_bytes(re_payload[8: 12], byteorder='big', signed=False) * 0.01
        mpb_ntc = int.from_bytes(re_payload[12: 16], byteorder='little', signed=True) / 2 ** 9
        trx_ntc = int.from_bytes(re_payload[16:], byteorder='little', signed=True) / 2 ** 9
        print('Lidar input voltage: {}\n'
              'Lidar input current: {}\n'
              'Temperature at Location 1: {}\n'
              'Temperature at Location 2: {}.'.format(input_valtage, input_current, mpb_ntc, trx_ntc))




    def ptc_sub_command_set_startup_standby_mode(self, fac_flag, mode='in operation'):
        cmd = 0xff
        fac_flag_byte = {'FAC': b'\x01', 'RELEASE': b'\x00'}[fac_flag.upper()]
        payload = b'\x00' + fac_flag_byte + b'\x00\x04'
        mode_byte = {'IN OPERATION': b'\x00', 'STANDBY': b'\x01'}[mode.upper()]
        payload += mode_byte
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)

    def ptc_command_ctl_microblaze(self, rw_flag, addr, value=b''):
        cmd = 0x13
        data = b'\xa0'
        if rw_flag == 'read':
            action = (0b01 << 4) + (0b10 << 2) + 0b1
        else:
            action = (0b10 << 4) + (0b10 << 2) + 0b1
        data += action.to_bytes(1, 'big')
        data += addr
        data += b'\x00\x01'
        if rw_flag == 'write':
            data += value
        crc32 = calCrc32(data)
        data += crc32.to_bytes(4, 'big')
        payload = data + b'\x00'
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)
        re_payload = final_response['response_payload']
        payload_value = re_payload[8: 12]
        print(payload_value.hex())
        return payload_value

    def ptc_command_ctl_microblaze_echo(self, rw_flag, addr):
        cmd = 0x13
        data = b'\xa0'
        if rw_flag == 'read':
            action = (0b01 << 4) + (0b10 << 2) + 0b1
        else:
            action = (0b10 << 4) + (0b10 << 2) + 0b1
        data += action.to_bytes(1, 'big')
        data += addr
        data += b'\x00\x01'
        if rw_flag == 'write':
            data += b'\x00\x00\x00\x05'
        crc32 = calCrc32(data)
        data += crc32.to_bytes(4, 'big')
        payload = data + b'\x00'
        final_response = self.ptc_sender(cmd, payload)
        print(final_response)

    def ptc_sub_command_set_fpga2_para(self, file):
        cmd = 0xff
        sub_cmd_code = 0x0001000E

        payload_file = open(file, 'rb').read()

        # piece_num =


    def ptc_file_sender(self, cmd, sub_cmd_code, payload_file):

        block_num = math.ceil(len(payload_file))

        print('block_num', block_num)
        data_index = 0
        block_index = 1

        while block_index <= block_num:
            if data_index + 1024 < len(payload_file):
                length = 1024
            else:
                length = len(payload_file) - data_index

            sub_data = payload_file[data_index: data_index + length]
            crc = crc_calc(sub_data)

            crc_valid_int = 1
            crc_valid_byte = crc_valid_int.to_bytes(4, byteorder='big')
            block_index_byte = block_index.to_bytes(4, byteorder='big')
            block_num_int = block_num + 1
            block_num_byte = block_num_int.to_bytes(4, byteorder='big')
            crc_byte = crc.to_bytes(4, byteorder='big')

            payload = sub_cmd_code


def read_ft_angle_calib(path):
    ft_a3_calibration_21 = np.dtype([
        ('eeff', 'S2'),
        ('protocol_version_major', 'u1'),
        ('protocol_version_minor', 'u1'),
        ('reserved', 'u2'),
        ('column_number', 'u1'),
        ('channel_number', 'u1'),
        ('resolution', 'u1'),
        ('azimuth_adjust', 'i4', 160 * 120),
        ('elevation_adjust', 'i4', 160 * 120),
        ('sha_256_value', 'u1', 32)
    ])
    with open(path, 'rb') as file_handle1:
        data = file_handle1.read()
    print(data)
    calib_data = np.frombuffer(data, dtype=ft_a3_calibration_21)
    print(len(data))
    angle_resolution = calib_data['resolution'][0]
    azimuth_adjust = (calib_data['azimuth_adjust'][0] * 0.01).reshape((160, 120))
    elevation_adjust = (calib_data['elevation_adjust'][0] * 0.01).reshape((160, 120))

    # 转ndarray为DataFrame
    angle_dtype = [
        ('channel', 'u1'),
        ('column_id', 'u1'),
        ('elevation', 'float64'),
        ('azimuth', 'float64'),
    ]
    angle_data = np.zeros(160 * 120, dtype=angle_dtype)
    angle_data['channel'] = np.tile(np.arange(1, 121), 160)
    angle_data['column_id'] = np.repeat(np.arange(0, 160), 120)
    angle_data['elevation'] = calib_data['elevation_adjust'][0] * 0.01
    angle_data['azimuth'] = calib_data['azimuth_adjust'][0] * 0.01
    df_correction = pd.DataFrame(angle_data)
    df_correction.columns = ['Channel', 'Column_id', 'Elevation', 'Azimuth']
    print(df_correction)
    return azimuth_adjust, elevation_adjust, df_correction


def angle_diagram(lidar_sn, angle_dataframe, save_path):
    fontsize = 18
    fig = plt.figure(figsize=(22, 9))
    fig.tight_layout()
    plt.subplots_adjust(wspace=0.2, hspace=0.25, right=0.8)
    ax = fig.add_subplot(111)
    ax.set_title('{}'.format(lidar_sn), fontsize=fontsize)
    ax.set_xlabel('Azimuth(°)', fontsize=fontsize * 0.6)
    ax.set_ylabel('Elevation(°)', fontsize=fontsize * 0.6)
    ax.scatter(angle_dataframe['Azimuth'], angle_dataframe['Elevation'], s=7.5)
    ax.grid()
    plt.show()
    # plt.savefig(os.path.join(save_path, '{}_angle_diagram.png'.format(lidar_sn)))


def calCrc32(data):
    crc_table = [
        0x00000000, 0x4c11db7, 0x9823b6e, 0xd4326d9, 0x130476dc, 0x17c56b6b, 0x1a864db2, 0x1e475005, 0x2608edb8, 0x22c9f00f, 0x2f8ad6d6,
        0x2b4bcb61, 0x350c9b64, 0x31cd86d3, 0x3c8ea00a, 0x384fbdbd, 0x4c11db70, 0x48d0c6c7, 0x4593e01e, 0x4152fda9, 0x5f15adac, 0x5bd4b01b,
        0x569796c2, 0x52568b75, 0x6a1936c8, 0x6ed82b7f, 0x639b0da6, 0x675a1011, 0x791d4014, 0x7ddc5da3, 0x709f7b7a, 0x745e66cd, 0x9823b6e0,
        0x9ce2ab57, 0x91a18d8e, 0x95609039, 0x8b27c03c, 0x8fe6dd8b, 0x82a5fb52, 0x8664e6e5, 0xbe2b5b58, 0xbaea46ef, 0xb7a96036, 0xb3687d81,
        0xad2f2d84, 0xa9ee3033, 0xa4ad16ea, 0xa06c0b5d, 0xd4326d90, 0xd0f37027, 0xddb056fe, 0xd9714b49, 0xc7361b4c, 0xc3f706fb, 0xceb42022,
        0xca753d95, 0xf23a8028, 0xf6fb9d9f, 0xfbb8bb46, 0xff79a6f1, 0xe13ef6f4, 0xe5ffeb43, 0xe8bccd9a, 0xec7dd02d, 0x34867077, 0x30476dc0,
        0x3d044b19, 0x39c556ae, 0x278206ab, 0x23431b1c, 0x2e003dc5, 0x2ac12072, 0x128e9dcf, 0x164f8078, 0x1b0ca6a1, 0x1fcdbb16, 0x18aeb13,
        0x54bf6a4, 0x808d07d, 0xcc9cdca, 0x7897ab07, 0x7c56b6b0, 0x71159069, 0x75d48dde, 0x6b93dddb, 0x6f52c06c, 0x6211e6b5, 0x66d0fb02,
        0x5e9f46bf, 0x5a5e5b08, 0x571d7dd1, 0x53dc6066, 0x4d9b3063, 0x495a2dd4, 0x44190b0d, 0x40d816ba, 0xaca5c697, 0xa864db20, 0xa527fdf9,
        0xa1e6e04e, 0xbfa1b04b, 0xbb60adfc, 0xb6238b25, 0xb2e29692, 0x8aad2b2f, 0x8e6c3698, 0x832f1041, 0x87ee0df6, 0x99a95df3, 0x9d684044,
        0x902b669d, 0x94ea7b2a, 0xe0b41de7, 0xe4750050, 0xe9362689, 0xedf73b3e, 0xf3b06b3b, 0xf771768c, 0xfa325055, 0xfef34de2, 0xc6bcf05f,
        0xc27dede8, 0xcf3ecb31, 0xcbffd686, 0xd5b88683, 0xd1799b34, 0xdc3abded, 0xd8fba05a, 0x690ce0ee, 0x6dcdfd59, 0x608edb80, 0x644fc637,
        0x7a089632, 0x7ec98b85, 0x738aad5c, 0x774bb0eb, 0x4f040d56, 0x4bc510e1, 0x46863638, 0x42472b8f, 0x5c007b8a, 0x58c1663d, 0x558240e4,
        0x51435d53, 0x251d3b9e, 0x21dc2629, 0x2c9f00f0, 0x285e1d47, 0x36194d42, 0x32d850f5, 0x3f9b762c, 0x3b5a6b9b, 0x315d626, 0x7d4cb91,
        0xa97ed48, 0xe56f0ff, 0x1011a0fa, 0x14d0bd4d, 0x19939b94, 0x1d528623, 0xf12f560e, 0xf5ee4bb9, 0xf8ad6d60, 0xfc6c70d7, 0xe22b20d2,
        0xe6ea3d65, 0xeba91bbc, 0xef68060b, 0xd727bbb6, 0xd3e6a601, 0xdea580d8, 0xda649d6f, 0xc423cd6a, 0xc0e2d0dd, 0xcda1f604, 0xc960ebb3,
        0xbd3e8d7e, 0xb9ff90c9, 0xb4bcb610, 0xb07daba7, 0xae3afba2, 0xaafbe615, 0xa7b8c0cc, 0xa379dd7b, 0x9b3660c6, 0x9ff77d71, 0x92b45ba8,
        0x9675461f, 0x8832161a, 0x8cf30bad, 0x81b02d74, 0x857130c3, 0x5d8a9099, 0x594b8d2e, 0x5408abf7, 0x50c9b640, 0x4e8ee645, 0x4a4ffbf2,
        0x470cdd2b, 0x43cdc09c, 0x7b827d21, 0x7f436096, 0x7200464f, 0x76c15bf8, 0x68860bfd, 0x6c47164a, 0x61043093, 0x65c52d24, 0x119b4be9,
        0x155a565e, 0x18197087, 0x1cd86d30, 0x29f3d35, 0x65e2082, 0xb1d065b, 0xfdc1bec, 0x3793a651, 0x3352bbe6, 0x3e119d3f, 0x3ad08088,
        0x2497d08d, 0x2056cd3a, 0x2d15ebe3, 0x29d4f654, 0xc5a92679, 0xc1683bce, 0xcc2b1d17, 0xc8ea00a0, 0xd6ad50a5, 0xd26c4d12, 0xdf2f6bcb,
        0xdbee767c, 0xe3a1cbc1, 0xe760d676, 0xea23f0af, 0xeee2ed18, 0xf0a5bd1d, 0xf464a0aa, 0xf9278673, 0xfde69bc4, 0x89b8fd09, 0x8d79e0be,
        0x803ac667, 0x84fbdbd0, 0x9abc8bd5, 0x9e7d9662, 0x933eb0bb, 0x97ffad0c, 0xafb010b1, 0xab710d06, 0xa6322bdf, 0xa2f33668, 0xbcb4666d,
        0xb8757bda, 0xb5365d03, 0xb1f740b4]

    crc = 0xffffffff
    for i in range(len(data)):
        crc = ((crc<<8)&0xffffffff) ^ crc_table[((crc>>24)^data[i])&0xff]

    return crc


def crc_calc(bytes):
    i_crc = 0xffffffff
    crc_table = crc_init()
    for byte in bytes:
        i_crc = ((i_crc << 8) & 0xffffffff) ^ \
            crc_table[(((i_crc >> 24) & 0xffffff) ^ byte) & 0xff]
    # print('crc:', i_crc)
    return i_crc


def crc_init():
    crc_table = []
    for i in range(0, 256):
        k = 0
        j = i << 24 | 0x800000
        while j != 0x80000000:
            k = ((k << 1) & 0xffffffff) ^ (0x04c11db7 if (k ^ j) & 0x80000000 else 0)
            j = (j << 1) & 0xffffffff
        crc_table.append(k)

    return crc_table



if __name__ == '__main__':
    lidar_host = '192.168.1.201'
    ptc_port = 9347
    # lidar_host = '172.16.4.57'
    # ptc_port = 42513
    # lidar_host = '192.168.1.201'
    # ptc_port = 9347
    # lidar_host = '172.16.4.67'
    # ptc_port = 42523
    PTC = PTC_CMD(lidar_host, ptc_port, network_card='')
    # --------A2角度文件--------
    # df_angle = PTC.ptc_command_get_lidar_calibration_a2()
    # azimuth_adjust, elevation_adjust, df_correction = read_ft_angle_calib(r'C:\Users\wanghaibo\Downloads\default_PandarFT.dat')
    # angle_diagram('FT_A2', df_correction, '')

    # --------A3角度文件--------
    # for _ in range(10):
    # *_, df_angle = PTC.ptc_command_get_lidar_calibration_a3()  # PTC获取角度文件
    #     time.sleep(0.5)
    # *_, df_angle = PTC.ptc_command_get_lidar_calibration_a3_slice()

    # *_, df_angle = read_ft_angle_calib(r'C:\Users\wanghaibo\Downloads\Angfile_A3_V2-0096_TRX311.dat')
    # angle_diagram('FT120_Angular_Distribution', df_angle, '')

    # --------

    # PTC.ptc_command_get_inventory_info_A3V2()
    # PTC.ptc_command_get_inventory_info_A3V3()
    # for _ in range(50):
    #     PTC.ptc_command_get_inventory_info_A3V3()

    PTC.ptc_command_get_config_info()

    # PTC.ptc_command_get_lidar_status()

    # PTC.ptc_command_get_register()

    # PTC.ptc_command_reboot()

    # -----------------Standby Mode-----------------
    # PTC.ptc_command_standby_mode('standby')
    # time.sleep(2)
    # PTC.ptc_command_standby_mode('In operation')


    # PTC.ptc_command_set_destination_ip(des_ip='192.168.1.100', port=2367, gps_port=10110, des_mac='FF:FF:FF:FF:FF:FF',
    #                                    src_ip='192.168.1.207', src_port=10000, src_mac='02:01:01:00:00:57')
    # PTC.ptc_command_set_control_port(ip='192.168.1.207', mask='255.255.255.0', gateway='192.168.1.1', vlan_flag='off',
    #                                  vlan_id=0, port=9347)
    # PTC.ptc_command_get_freeze_frame_info()
    # PTC.ptc_command_set_freeze_frame_clear()

    # PTC.ptc_sub_command_shutdown_protection('fac')
    # PTC.ptc_sub_command_set_sn('fac', 'FT120-A366668889')
    # PTC.ptc_sub_command_set_pn('fac', 'FT120-A3')  # TODO not supported yet
    # PTC.ptc_sub_command_set_mac_address('fac', '00:11:22:33:44:55')  # TODO not supported yet

    # -----------------角度文件------------------------
    # PTC.ptc_sub_command_set_lidar_angle_cali('fac', r'D:\WORK\FT\PreDV\Angfile_A3_testsft0.dat')  # TODO

    # PTC.ptc_sub_command_control_watchdog('fac', 2000000)

    # -----------------sleep模式----------------------
    # PTC.ptc_sub_command_sleep_mode('release', 10000)

    # -----------------帧率设置------------------------
    # PTC.ptc_sub_command_set_frame_rate('fac', 10)  # 写flash，断电保留
    # PTC.ptc_sub_command_get_frame_rate('release')
    # PTC.ptc_sub_command_set_customer_frame_rate('release', 20)  # 实时生效断电不保留，for 客户

    # -----------------回波模式设置---------------------
    # PTC.ptc_command_set_return_mode('strongest return')  # 写flash，断电保留，实时生效
    # PTC.ptc_sub_command_set_customer_return_mode('release', 'first return')  # 实时生效断电不保留，客户
    # PTC.ptc_sub_command_set_customer_return_mode('release', 'strongest return')  # 实时生效断电不保留，客户
    # PTC.ptc_sub_command_set_customer_return_mode('release', 'first and strongest return')  # 实时生效断电不保留，客户

    # -----------------配置左右雷达--------------------- 
    # PTC.ptc_sub_command_set_lidar_position('fac', 'right')
    PTC.ptc_sub_command_get_lidar_position('release')

    # -----------------GET MCU DEBUG INFO-------------
    # PTC.ptc_sub_command_get_mcu_debug_info('fac')

    # -----------------设置\获取PTP-------------------------
    # PTC.ptc_command_set_ptp_config('enable', '802.1AS-autosar', 2, 'L2', 'TSN')
    # PTC.ptc_command_set_ptp_config('enable', '802.1AS-automotive', 0, 'L2', 'TSN')
    # print(PTC.ptc_command_get_ptp_config())

    # PTP状态获取
    # ptp_query_type = 'PTP STATUS'
    # for _ in range(20):
    #     print('Loop{}'.format(_))
    #     PTC.ptc_command_ptp_diagnostics(ptp_query_type)
    #     time.sleep(0.2)
    # -----------------清除NVM flash-------------------
    # re_code = PTC.ptc_sub_command_clear_nvm_area('fac')
    # print(re_code)
    #
    # -----------------更改点云网络参数------------------
    # effective_flag = 1  # 0: 非立即生效  1: 立即生效
    # nvm_flag = 0  # 0: 不写nvm 1: 写nvm
    #
    # srcIP = '192.168.1.201'
    # srcPort = 9347
    # srcMac = '02:00:00:00:14:06'
    #
    # destIP = '255.255.255.255'
    # destPort = 2368
    # destMac = 'ff:ff:ff:ff:ff:ff'
    #
    # netMask = '255.255.255.0'
    # gateway = '192.168.1.1'
    #
    # vlan_flag = 0
    # vlan_id = 0
    # #
    # PTC.ptc_sub_command_set_customer_udp_para('release', srcIP, srcPort, srcMac, destIP, destPort, destMac, netMask,
    #                                           gateway, vlan_flag, vlan_id)

    # PTC.ptc_sub_command_set_para('fac', srcIP, srcPort, srcMac, destIP, destPort, destMac, netMask, gateway, vlan_flag,
    #                              vlan_id)
    # #
    # PTC.ptc_sub_command_get_para('fac', 'TCP')

    # -----------------GET MODE FAULT INFO-------------
    # PTC.ptc_command_get_mode_fault_info()

    # -----------------清除时间统计信息-------------------
    # PTC.ptc_sub_command_set_clear_time_statistic('fac')

    # -----------------Sync Angle----------------------
    PTC.ptc_command_set_sync_angle('on', 40)
    #
    # -----------------获取ADC数据-----------------------
    # PTC.ptc_sub_command_get_adc('release')

    # -----------------读取寄存器值-----------------------
    # value = PTC.ptc_command_ctl_microblaze('read', b'\x01\00\x02\x20')
    # value = '0x' + value.hex()
    # print(value)

    # -----------------开启雷达echo模式-------------------
    # PTC.ptc_command_ctl_microblaze_echo('write', b'\x00\x00\x00\xc0')

    # -----------------上电默认standby模式----------------
    # PTC.ptc_sub_command_set_startup_standby_mode('release', mode='in operation')

    # PTC.ptc_command_get_freeze_frame_info()


    # 上传大文件的指令
    # file_path = r'C:\Users\wanghaibo\Downloads\C_FT38CA519338CA51_1.00.34p_c8246396_refcalib.param'
    # PTC.ptc_sub_command_set_fpga2_para(file_path)

    # PTC.get_lidar_monitor('release')


