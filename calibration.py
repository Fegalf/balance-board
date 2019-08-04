# -*- coding: utf-8 -*-

from BalanceBoard import Text, time
from mpu6050_interface import MPU6050
from graphics import *
import numpy as np

def run_calibration():
    dt = 0.023
    # Initialize MPU6050 
    mpu6050 = MPU6050()
    nb_mesures = 0
    accumul_x = 0
    accumul_y = 0
    accumul_gyrox = 0
    accumul_gyroy = 0
    now = time.time()
    t = 0

    data = []
    while (t<3):
        t = time.time()-now
        x_rotation, y_rotation, _, x_gyro,y_gyro = mpu6050.read_data()
        data.append([x_rotation, y_rotation, x_gyro, y_gyro])

    data = np.array(data)
    rotation_offset_x, rotation_offset_y, accumul_gyrox, accumul_gyroy = data.mean(axis=0)
    return rotation_offset_x, rotation_offset_y, accumul_gyrox, accumul_gyroy