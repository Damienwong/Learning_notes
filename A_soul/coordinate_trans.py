#-*- coding: utf-8 -*-
'''
Author: shaobaineng kuangsongyang
Date: 2021-04-23 20:58:30
LastEditors: Please set LastEditors
LastEditTime: 2021-08-09 14:12:34
Description: 以雷达中心为原点，只考虑旋转转换，大地坐标系的原点和雷达中心的原点重合, 
笛卡尔坐标系的y轴正向与球坐标系下的水平0度、俯仰0度方向重合，笛卡尔坐标系的z轴正向和球坐标系下的俯仰90方向重合，笛卡尔坐标系的x轴正向和球坐标系下的水平90度，俯仰0度方向重合
球坐标系的表达式为(d,a,b),其中d为距离，a为俯仰角，b为水平角
旋转的正方向为朝X，Y，Z 的正方向看过去时的顺时针，注意Z轴的旋转正方向为角度变小的方向
'''

import math
import numpy as np

#用于雷达的水平角度转换
#x,y可以是numpy array,list或数字
#输出的是角度值
def xy2azi(x,y):
    return np.mod((450-np.mod(np.degrees(np.arctan2(y,x)),360)),360)

#输入球坐标，可以是二维numpy array或list，numpy array为N*3的格式，如np.array([[1,2,3],[3,4,5]])，[[1,2,3],[3,4,5]]，[1,2,3]
#输出为numpy array
def sph2xyz(sph):
    sph = np.array(sph)
    if sph.shape == (3,):
        point = np.zeros(sph.shape)
        azi= np.radians(sph[2])
        ele =np.radians(sph[1])  
        d = sph[0]
        point[0] = d*np.cos(ele)*np.sin(azi)
        point[1]  = d*np.cos(ele)*np.cos(azi)
        point[2] = d*np.sin(ele)
        return point
    else:        
        points = np.zeros(sph.shape)
        azi= np.radians(sph[:,2])
        ele =np.radians(sph[:,1])  
        d = sph[:,0]
        points[:,0] = d*np.cos(ele)*np.sin(azi)
        points[:,1]  = d*np.cos(ele)*np.cos(azi)
        points[:,2] = d*np.sin(ele)
        return points

#输入x,y,z坐标，可以是二维numpy array或x,y,z的list，numpy array为N*3的格式，如np.array([[1,2,3],[3,4,5]])，[[1,2,3],[3,4,5]]，[1,2,3]
#输出为numpy array
def xyz2sph(xyz):
    xyz = np.array(xyz)
    if xyz.shape == (3,):
        point =  np.zeros(xyz.shape)
        xy = xyz[0]**2 + xyz[1]**2 
        point[0] = np.sqrt(xy + xyz[2]**2)   
        point[1] = np.degrees(np.arctan2(xyz[2],np.sqrt(xy))) 
        point[2] = xy2azi(xyz[0], xyz[1])
        return point               
    else:
        points =  np.zeros(xyz.shape)
        xy = xyz[:,0]**2 + xyz[:,1]**2 
        points[:,0] = np.sqrt(xy + xyz[:,2]**2)    
        points[:,1] = np.degrees(np.arctan2(xyz[:,2],np.sqrt(xy))) 
        points[:,2] = xy2azi(xyz[:,0], xyz[:,1])
        return points


#用于雷达的旋转，旋转前输入的x,y,z和旋转后输出的x,y,z都是在雷达坐标系下某个固定的点在大地坐标系下的坐标，实际使用时，一身旋转前或旋转后，雷达坐标系与大地坐标系重合
#输入x,y,z坐标，可以是二维numpy array或x,y,z的list，numpy array为N*3的格式，如np.array([[1,2,3],[3,4,5]])，[[1,2,3],[3,4,5]]，[1,2,3]
#输入为绕x,y,z轴旋转的角度值，如果
#由于绕x,y,z轴旋转的顺序不一样，会导致结果不一样，因此，只支持单次旋转一个轴
#输出为numpy array
def coordinate_rotation(points_xyz,axis,rotation_angle):
    points_xyz_mat = np.mat(points_xyz)
    if axis == 'x' or axis == 'X':
        roll = np.radians(rotation_angle)
        Rx = np.mat([[1,0,0],[0,np.cos(roll),-np.sin(roll)],[0,np.sin(roll),np.cos(roll)]])
        points =Rx*(np.transpose(points_xyz_mat))     
    elif axis == 'y' or axis == 'Y':
        pitch =  np.radians(rotation_angle)
        Ry = np.mat([[np.cos(pitch),0,np.sin(pitch)],[0,1,0],[-np.sin(pitch),0,np.cos(pitch)]])
        points = Ry*(np.transpose(points_xyz_mat))
    elif axis == 'z' or axis == 'Z':
        yaw = np.radians(rotation_angle)
        Rz = np.mat([[np.cos(yaw),-np.sin(yaw),0],[np.sin(yaw),np.cos(yaw),0],[0,0,1]])
        points = Rz*(np.transpose(points_xyz_mat))    
    else:
        print('asix error from coordinate_trnas')
        return None
    return np.array(np.transpose(points))

def coordinate_rotation_sph(point_sph,axis,rotation_angle):
    point_xyz =  sph2xyz(point_sph)
    point_xyz_t = coordinate_rotation(point_xyz,axis,rotation_angle)
    point_sph_t = xyz2sph(point_xyz_t)
    return(point_sph_t)

#雷达移动move_xyz，即雷达在大地坐标系下的坐标
def coordinate_translation(points_xyz,move_xyz):
    points_xyz = np.array(points_xyz)
    if  points_xyz.shape == (3,):
        points_xyz[0] -= move_xyz[0]
        points_xyz[1] -= move_xyz[1]
        points_xyz[2] -= move_xyz[2]
        return points_xyz             
    else:
        points_xyz[:,0] -= move_xyz[0]
        points_xyz[:,1] -= move_xyz[1]
        points_xyz[:,2] -= move_xyz[2]
        return points_xyz

def coordinate_translation_sph(points_sph,move_xyz):
    points_xyz =  sph2xyz(points_sph)
    points_xyz_t = coordinate_translation(points_xyz,move_xyz)
    points_sph_t = xyz2sph(points_xyz_t)
    return(points_sph_t)


if __name__  == "__main__":
    dis_ele_azi = [0.1, 23, 90]
    # dis_ele_azi1 = coordinate_rotation_sph(dis_ele_azi, 'z', np.rad2deg(np.arctan(1 / 2 ** 0.5)))

    # dis_ele_azi1 = coordinate_rotation_sph(dis_ele_azi, 'y',  24.3)
    # print(dis_ele_azi1)
    dis_ele_azi2 = coordinate_rotation_sph(dis_ele_azi, 'z', 94-90)
    print(dis_ele_azi2)
    # cord = [0.004, -8.988, -0.477]
    # print(xyz2sph(cord))
    # a = np.array([[1, 2, 3, 4], [1, 2, 3, 5], [3, 4, 5, 5]])world_cordinate_temp
    # a = a.T
    # point = coordinate_rotation_sph(a, 'x', -45)
    # print(point)
    # print(a[:, 0])
    #  # elevations = list(range(52))
    #   d = 1
    #   elevation = 25
    #   azimuth_start = 0
    #   dis,ele,azi = coordinate_rotation_sph([d,elevation,azimuth_start],'y', 1)[0]
    # #  dis,ele,azi = coordinate_rotation_sph([d,elevation,azimuth_start],'x', -25)[0]
    #   print(ele,azi)
    # import pandas as pd
    # datas_type = [('a', 'u2'),
    #               ('b', 'float64'),
    #               ('c', 'float64')]
    # datas1 = np.zeros(10, datas_type)
    # datas1['a'] = np.arange(10)
    # datas1['b'] = np.random.rand(10)
    # datas1['c'] = np.random.rand(10)
    #
    # datas_a = datas1[(datas1['a'] >= 5) | (datas1['a'] == 1)]
    #
    # print(datas1)
    # print(datas_a)
    # print(datas_b)



