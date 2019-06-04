#!/usr/bin/python
# -*- coding: latin-1 -*-
from smbus2 import SMBus
import math
from graphics import *
import time
import matplotlib.pyplot as plt
import numpy as np

class MPU6050:
    def __init__(self,):
        self.bus = SMBus(1)
        self.address = 0x68
        self.bus.write_byte_data(self.address, 0x6b, 0)
        self.bus.write_byte_data(self.address, 26, 3)

    def read_data(self,):
        raw_data = self.bus.read_i2c_block_data(self.address, 0x3B, 14)
        acc_x = (raw_data[0] << 8) + raw_data[1]

        if acc_x >= 0x8000:
            acc_x = -((65535 - acc_x) + 1)
        acc_x = acc_x / 16384.0
        acc_y = (raw_data[2] << 8) + raw_data[3]

        if acc_y >= 0x8000:
            acc_y = -((65535 - acc_y) + 1)
        acc_y = acc_y / 16384.0
        acc_z = (raw_data[4] << 8) + raw_data[5]

        if acc_z >= 0x8000:
            acc_z = -((65535 - acc_z) + 1)

        acc_z = acc_z / 16384.0
        z2 = acc_z * acc_z
        x_rot = math.degrees(math.atan2(acc_y, math.sqrt((acc_x * acc_x) + z2)))
        y_rot = -math.degrees(math.atan2(acc_x, math.sqrt((acc_y * acc_y) + z2)))
        gyro_x = (raw_data[8] << 8) + raw_data[9]

        if gyro_x >= 0x8000:
            gyro_x = -((65535 - gyro_x) + 1)

        gyro_x = gyro_x / 131.0
        gyro_y = (raw_data[10] << 8) + raw_data[11]

        if gyro_y >= 0x8000:
            gyro_y = -((65535 - gyro_y) + 1)
        gyro_y = gyro_y / 131.0

        return x_rot, y_rot, acc_z, gyro_x, gyro_y

mpu6050 = MPU6050()

dt = 0.01    # To be verified: what is sampling rate?
K = 0.98
K1 = 1 - K

nomDuFichier = './mesures/mesures.csv'
fichierData = open(nomDuFichier, 'w')

# Start coordinates.
x_prec = 0
y_prec = 0
gain = largeur/90 # 90degrés font la pleine largeur d'affichage

x_rotation, y_rotation, accel_zout, x_gyro, y_gyro = mpu6050.read_data()
angle_x_filtre = x_rotation
angle_y_filtre = y_rotation
gyro_offset_x = x_gyro
gyro_offset_y = y_gyro
gyro_total_x = (angle_x_filtre) - gyro_offset_x
gyro_total_y = (angle_y_filtre) - gyro_offset_y

t0 = time.time()
next_t = dt

while (clickPoint == None):
    t = time.time()-t0
    x_rotation, y_rotation, accel_zout, x_gyro, y_gyro = mpu6050.read_data()

    gyro_x_delta = dt*(x_gyro-gyro_offset_x)
    gyro_y_delta = dt*(y_gyro-gyro_offset_y)
    gyro_total_x = gyro_total_x + gyro_x_delta
    gyro_total_y = gyro_total_y + gyro_y_delta

    angle_x_filtre = K * (angle_x_filtre + gyro_x_delta) + (K1 * x_rotation)
    angle_y_filtre = K * (angle_y_filtre + gyro_y_delta) + (K1 * y_rotation)

    cir.move(gain*(angle_x_filtre-x_prec), gain*(angle_y_filtre-y_prec))
    
    fichierData.write("{0:10f}, {1:4.1f}, {2:4.1f}, {3:4.1f}, {4:4.1f}, "
                      "{5:4.1f}, {6:4.1f}\n".format(t, x_rotation, y_rotation,
                                                    gyro_total_x, gyro_total_y,
                                                    angle_x_filtre,angle_y_filtre))
    x_prec = angle_x_filtre
    y_prec = angle_y_filtre
    next_t = next_t + dt

fichierData.close()
print("Les mesures sont dans ", nomDuFichier)

# On relie le fichier
fichierData = open(nomDuFichier, 'r')
temps = []
angleX = []
angleY = []
accX = []
accY = []
gyroX = []
gyroY = []

for x in fichierData:
  ledata = [float(y) for y in x.split(', ')]
  temps.append(ledata[0])
  accX.append(ledata[1])
  accY.append(ledata[2])
  gyroX.append(ledata[3])
  gyroY.append(ledata[4])
  angleX.append(ledata[5])
  angleY.append(ledata[6])

fichierData.close()

# Ploting some graphs
plt.figure(1)  
plt.subplot(221)
plt.plot(temps, angleX)
plt.xlabel('temps [sec]')
plt.ylabel('angle X [deg]')
plt.grid(True)
plt.subplot(222)
plt.hist(angleX, 50, density=1, facecolor='g', alpha=0.75)
plt.xlabel('angle X [deg]')
plt.title("$\mu_x$={0:4.1f}$^\circ$, $\sigma_x$={1:4.1f}$^\circ$".format(np.mean(angleX), np.std(angleX)))
plt.grid(True)
plt.subplot(223)
plt.plot(temps,angleY)
plt.xlabel('temps [sec]')
plt.ylabel('angle Y [deg]')
plt.grid(True)
plt.subplot(224)
plt.hist(angleY, 50, density=1, facecolor='g', alpha=0.75)
plt.xlabel('angle Y [deg]')
plt.title("$\mu_y$={0:4.1f}$^\circ$, $\sigma_y$={1:4.1f}$^\circ$".format(np.mean(angleY),np.std(angleY)))
plt.grid(True)



plt.figure(2)
plt.subplot(211)
plt.plot(temps, angleX, temps, gyroX, temps, accX)
plt.xlabel('temps [sec]')
plt.ylabel('angle X [deg]')
plt.grid(True)
plt.title('Les angles')
plt.subplot(212)
plt.plot(temps, angleY, temps, gyroY, temps, accY)
plt.xlabel('temps [sec]')
plt.ylabel('angle Y [deg]')
plt.grid(True)
plt.show()

