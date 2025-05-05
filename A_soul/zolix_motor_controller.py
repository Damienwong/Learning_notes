# -*- coding: UTF-8 -*-
"""
@func: motor control to make the channels aim the target
"""
import platform
import time

import serial
import serial.tools.list_ports


class zolix_control:
    def __init__(self, port_name='COM12'):
        if 1:
            self.zolix = serial.Serial(port=port_name,baudrate=19200,parity='N',bytesize=8,stopbits=1,timeout=10)
            # print('zolix=',self.zolix)
            # print('self.zolix.isOpen() = ',self.zolix.isOpen())
            # print()

            if self.zolix.isOpen():
                self.zolix.flushOutput()
                self.zolix.write('VE\r'.encode())
                
                data = self.readSerData()
                print('hello4')
                print('connect with controller successfully!')
                print('Controller Info: ',data)
##                self.zolix.flushInput()
                self.zolix.flushOutput()
                print('ID:',self.get_ID())
                print('')
        # except:               
        #     print('Cannot connected to the Serial: ', port_name)
        #     port_list = list(serial.tools.list_ports.comports())
        #     print('Available COM: ')
        #     for i in range(len(port_list)):
        #         print(port_list[i])

    def get_Version(self):
        self.zolix.flushOutput()
        command = 'VE\r'
        self.zolix.write(command.encode())
        vers=self.readSerData()
##        print 'Controller ID: ', vers
        return vers

    def get_ID(self):
        self.zolix.flushOutput()
        command = 'ID\r'
        self.zolix.write(command.encode())
        ID=self.readSerData()
##        print 'Controller ID: ', ID
        return ID

    def get_topSpeed(self, axis):
        command = axis.upper() + 'V' + '\r'
        self.zolix.flushOutput()
        self.zolix.write(command.encode())
        data = self.readSerData()

        if data == 'E0\r' or data == 'E1\r' or data == 'ER\r':
            print('Error:', data)
        else:
            result = data.split(',')
            speed = result[-1]
            print('axis', axis, 'top_speed:', speed)

        
    def set_topSpeed(self,axis,speed):
        command = 'V'+axis.upper()+','+str(speed)+'\r'
##        print 'set_topSpeed command:',[command]
        self.zolix.flushOutput()
        self.zolix.write(command.encode())
        data=self.readSerData()
        if data=='OK\r':
            print('set axs', axis, 'speed:',speed)
        elif data == 'E0\r' or data == 'E1\r' or data == 'ER\r':
            print('Error:' ,data)
        else:
            print('unexpected error!')

    def get_accSpeed(self, axis):
        command = axis.upper() + 'A' + '\r'
        self.zolix.flushOutput()
        self.zolix.write(command.encode())
        data = self.readSerData()

        if data == 'E0\r' or data == 'E1\r' or data == 'ER\r':
            print('Error:', data)
        else:
            result = data.split(',')
            acc = result[-1]
            print('axis', axis, 'acc:', acc)


    def set_accSpeed(self,axis,accSpeed):
        command = 'A'+axis.upper()+','+str(accSpeed)+'\r'
##        print 'set_accSpeed command:',[command]
        self.zolix.flushOutput()
        self.zolix.write(command.encode())
        data = self.readSerData()
        if data == 'OK\r':
            print('set axs', axis, 'accSpeed:',accSpeed)
        elif data == 'E0\r' or data == 'E1\r' or data == 'ER\r':
            print('Error: ', data)
        else:
            print('unexpected error!')


    def set_initSpeed(self,axis,initSpeed):
        command = 'F'+axis.upper()+','+str(initSpeed)+'\r'
##        print 'set_initSpeed command:',[command]
        self.zolix.flushOutput()
        self.zolix.write(command.encode())
        data = self.readSerData()
        if data == 'OK\r':
            print('set axs', axis, 'accSpeed:',initSpeed)
        elif data == 'E0\r' or data == 'E1\r' or data == 'ER\r':
            print('Error: ', data)
        else:
            print('unexpected error!')       

    def goHome(self, axis):
        command = 'H'+axis.upper()+'\r'
        self.zolix.flushOutput()
        self.zolix.write(command.encode())
        data = self.readSerData()
        dataExpected = '?'+axis.upper()+',0\r'
        if data == dataExpected:
            print('axis',axis,'at Home!')
        elif data == 'ER\r':
            print('ERROR', data)
        else:
            print('Unexpeted error!')

    def move(self, axis, shift):
        pos = ''
        if shift > 0:
            command = '+'+ axis.upper() + ',' + str(shift) + '\r'
            # print('command = ',command)
            self.zolix.flushOutput()
            self.zolix.write(command.encode())
            data = self.readSerData()

        elif shift<0:
            command = '-'+ axis.upper() + ',' + str(-1*shift) + '\r'
            self.zolix.flushOutput()
            self.zolix.write(command.encode())
            data = self.readSerData()
        else:
            data='No movement'
        if data=='ER\r':
            print ('move ER:',data)
        else:
            pos = self.position(axis)
#            print axis, ': ',pos
            return pos


    # def test(self):
    #     self.zolix.write(go_home)
    #     time.sleep(0.1)
    #     self.move('Y',5000)
    #     time.sleep(0.1)

    def close(self):
        self.zolix.close()

    def posation(self,axis):
        return self.position(axis)

    def position(self,axis):
        pos = ''
        command = '?'+axis.upper()+'\r'
        self.zolix.flushOutput()
        self.zolix.write(command.encode())
        data = self.readSerData()
        place = int(data[3:])
        # print 'the position is' + pos
        return place

    def readSerData(self):
        data=''
        for i in range(100):
            s = self.zolix.read().decode()
            data = data+s
            if s == '\r':
                break
        return data


class MotorControl:
    def __init__(self, com='ttyUSB0'):
        self.com = com
        self.zc = zolix_control(com)
        self.presentAngle = 0
        self.presentAngle_x = 0

    def moveByordr(self, angle, flag='Y'):
        if flag.upper() == 'Y':
            shiftAngle = - angle * 800 - self.presentAngle
            angleNew = self.zc.move('Y', round(shiftAngle))
            self.presentAngle = - angle * 800
        else:
            shiftAngle = - angle * 800 - self.presentAngle_x
            angleNew = self.zc.move('X', round(shiftAngle))
            self.presentAngle_x = - angle * 800

    def goInit(self):
        shiftAngle = - self.presentAngle
        shiftAngle_x = - self.presentAngle_x
        angleNew = self.zc.move('Y', round(shiftAngle))
        angleNew_x = self.zc.move('X', round(shiftAngle_x))
        self.presentAngle = 0
        self.presentAngle_x = 0

    def get_position(self):
        pos_y = self.zc.position('Y')
        pos_x = self.zc.position('X')
        # print(' Zolix Motor Y Position: {}.\n'.format(pos_y),
        #       'Zolix Motor X Position: {}.'.format(pos_x))
        return pos_y, pos_x

    def point_forward(self):
        pos_y, pos_x = self.get_position()
        self.zc.move('Y', -pos_y)
        self.zc.move('X', -pos_x)
        self.get_position()
        self.presentAngle = 0
        self.presentAngle_x = 0
        print('Make Zolix point forward successfully.\n')

    def motor_init(self):
        self.zc.goHome('Y')
        self.zc.move('Y', 86.6 * 800)
        self.zc.goHome('X')
        self.zc.move('X', 86 * 800)


if __name__ == "__main__":
    sys = platform.system().upper()
    com = ''
    if sys == 'WINDOWS':
        com = 'com22'
    elif sys == 'LINUX':
        com = '/dev/ttyUSB0'

    mc = MotorControl(com)
    # mc.motor_init()
    mc.moveByordr(-45, 'X')
    # time.sleep(5000)
    # mc.goInit()
    # mc.zc.goHome('X')
    # mc.zc.set_accSpeed('x', 12500)
    # mc.zc.goHome('Y')
    # mc.moveByordr(-86, 'X')
    # mc.moveByordr(-86.6, 'Y')
    # mc1 = MotorControl(com)


    # time.sleep(00)
    # print(mc.presentAngle)
    # mc.point_forward()
    # mc.moveByordr(10, 'Y')
    # mc.moveByordr(5, 'Y')
    # mc.point_forward()
    # print(mc.presentAngle)

