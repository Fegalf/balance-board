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
    next_t = 0
    while (t<3):
        t = time.time()-now
        x_rotation, y_rotation,_,x_gyro,y_gyro = mpu6050.read_data()
        print(x_rotation, y_rotation,_,x_gyro,y_gyro )

        nb_mesures += 1
        accumul_x += x_rotation
        accumul_y += y_rotation
        accumul_gyrox += x_gyro
        accumul_gyroy += y_gyro

        next_t += dt
        pause = next_t-(time.time()-now)
        if (pause>0):
            time.sleep(pause)


    rotation_offset_x = accumul_x / nb_mesures
    rotation_offset_y = accumul_y / nb_mesures
    accumul_gyrox = accumul_gyrox / nb_mesures
    accumul_gyroy = accumul_gyroy / nb_mesures

    return rotation_offset_x, rotation_offset_y, accumul_gyrox, accumul_gyroy