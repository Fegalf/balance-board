# -*- coding: utf-8 -*-

from BalanceBoard import Timer, EmptyCircle, Text, Cursor, DataFile, plot_session_graphs, display_congrats, time
from mpu6050_interface import MPU6050
from graphics import *
import numpy as np

def run_calibration():
    dt = 0.023    # à vérifier quelle est la fréquence d'échantillonage
    timeCt = 0.5 # à tester

    def comp_filter(acc,rate):
        return

    def mesure_offset_gyro():
        dt = 0.01
        gyro_total_x = 0
        gyro_total_y = 0
        next_t = time.time()
        for ii in range(100):
            x_rotation, y_rotation,accel_zout,x_gyro,y_gyro = mpu6050.read_data()

            gyro_total_x = gyro_total_x + dt*x_gyro
            gyro_total_y = gyro_total_y + dt*y_gyro

            next_t = next_t + dt
            pause = next_t-time.time()
            if (pause>0):
                time.sleep(pause)

        gyro_offset_x = gyro_total_x
        gyro_offset_y = gyro_total_y
        return gyro_offset_x, gyro_offset_y 

    K = 0.98
    K1 = 1 - K

    #Dessin de la zone graphique
    largeur = 800
    hauteur = 800
    win = GraphWin("Angle de la planche", largeur, hauteur)
    #win.yUp()
    pt = Point(largeur/2, hauteur/2)
    cir0 = Circle(pt,largeur*15/90)
    cir0.setOutline("yellow")
    cir0.draw(win)
    cir1 = Circle(pt,largeur*5/90)
    cir1.setOutline("green")
    cir1.draw(win)
    linh = Line(Point(largeur/2,hauteur-30),Point(largeur/2,30))
    linh.draw(win)
    linv = Line(Point(30,hauteur/2),Point(largeur-30,hauteur/2))
    linv.draw(win)
    cir = Circle(pt, 8)
    cir.setFill("green")
    #cir.setOutline("yellow")
    #cir.setWidth(2)
    cir.draw(win)

    #label = Text(Point(100, 120), 'Du texte')
    #label.draw(win)

    message = Text(Point(win.getWidth()/2, 10), "Laisser immobile le dispositif pendant au moins 4 secondes.")
    message.draw(win)
    #win.getMouse()

    # Initialize MPU6050 
    mpu6050 = MPU6050()

    x_rotation, y_rotation,accel_zout,x_gyro,y_gyro = mpu6050.read_data()

    print("Avant tout: X={0:4.1f} deg, Y={1:4.1f} deg, z={2:4.1f} g, gyro_X={3:4.1f}, gyro_Y={4:4.1f}".format(x_rotation, y_rotation,accel_zout,x_gyro,y_gyro))

    print("---------------------")

    gyro_offset_x, gyro_offset_y = mesure_offset_gyro();

    # Coordonnées de départ au centre
    x_prec = 0
    y_prec = 0
    gain = largeur/90 # 90degrés font la pleine largeur d'affichage

    now = time.time()
    x_rotation, y_rotation,accel_zout,x_gyro,y_gyro = mpu6050.read_data()
    angle_x_filtre = x_rotation
    angle_y_filtre = y_rotation
    gyro_total_x = (angle_x_filtre) - gyro_offset_x
    gyro_total_y = (angle_y_filtre) - gyro_offset_y

    next_t = dt

    pause = next_t-(time.time()-now)
    if (pause>0):
        time.sleep(pause)
        
    nb_mesures = 0
    accumul_x = 0
    accumul_y = 0
    t = 0
    while (t<3):
        t = time.time()-now
        x_rotation, y_rotation,accel_zout,x_gyro,y_gyro = mpu6050.read_data()

        nb_mesures += 1
        accumul_x += x_rotation
        accumul_y += y_rotation

        gyro_x_delta = dt*(x_gyro-gyro_offset_x)
        gyro_y_delta = dt*(y_gyro-gyro_offset_y)
        gyro_total_x = gyro_total_x + gyro_x_delta
        gyro_total_y = gyro_total_y + gyro_y_delta

        angle_x_filtre = K * (angle_x_filtre + gyro_x_delta) + (K1 * x_rotation)
        angle_y_filtre = K * (angle_y_filtre + gyro_y_delta) + (K1 * y_rotation)

        cir.move(gain*(angle_x_filtre-x_prec),gain*(angle_y_filtre-y_prec))
        
        x_prec = angle_x_filtre
        y_prec = angle_y_filtre

        next_t = next_t + dt
        pause = next_t-(time.time()-now)
        if (pause>0):
            time.sleep(pause)


    win.close()

    rotation_offset_x = accumul_x / nb_mesures
    rotation_offset_y = accumul_y / nb_mesures

    print("Calibration: X_offset={0:4.1f} deg, Y_offset={1:4.1f} deg, gyro_X_offset={2:4.1f}, gyro_Y_offset={3:4.1f}".format(rotation_offset_x, 
                                                                                                                         rotation_offset_y,
                                                                                                                         gyro_offset_x, 
                                                                                                                         gyro_offset_y))
    return rotation_offset_x, rotation_offset_y, gyro_offset_x, gyro_offset_y