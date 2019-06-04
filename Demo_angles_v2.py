#!/usr/bin/python
#import smbus
from smbus2 import SMBus
import math
#import graphics
from graphics import *
import time
import matplotlib.pyplot as plt
import numpy as np

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

# scaling factors for MPU6050
#gyro_scale = 131.0
#accel_scale = 16384.0


def read_byte(reg):
    return bus.read_byte_data(address, reg)


def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg + 1)
    value = (h << 8) + l
    return value


def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

 
def dist(a, b):
    return math.sqrt((a*a)+(b*b))


def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)


def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)


dt = 0.01    # To be verified: what is sampling rate?
timeCt = 0.5 # To be tested

def comp_filter(acc, rate):
    return


def lit_tout_MPU6050(addr):
    raw_data = bus.read_i2c_block_data(addr,0x3B,14)
    acc_x =  (raw_data[0] << 8) + raw_data[1]

    if acc_x >= 0x8000:
        acc_x = -((65535 - acc_x) + 1)
    acc_x = acc_x / 16384.0
    acc_y =  (raw_data[2] << 8) + raw_data[3]

    if acc_y >= 0x8000:
        acc_y = -((65535 - acc_y) + 1)
    acc_y = acc_y / 16384.0
    acc_z =  (raw_data[4] << 8) + raw_data[5]

    if acc_z >= 0x8000:
        acc_z = -((65535 - acc_z) + 1)

    acc_z = acc_z / 16384.0
    z2 = acc_z*acc_z
    x_rot = math.degrees(math.atan2(acc_y, math.sqrt((acc_x*acc_x)+z2)))
    y_rot = -math.degrees(math.atan2(acc_x, math.sqrt((acc_y*acc_y)+z2)))
    gyro_x = (raw_data[8] << 8) + raw_data[9]

    if gyro_x >= 0x8000:
        gyro_x = -((65535 - gyro_x) + 1)

    gyro_x = gyro_x / 131.0
    gyro_y =  (raw_data[10] << 8) + raw_data[11]

    if gyro_y >= 0x8000:
        gyro_y = -((65535 - gyro_y) + 1)
    gyro_y = gyro_y / 131.0

    #gyro_z =  (raw_data[12] << 8) + raw_data[13]
    #if (gyro_z >= 0x8000):
    #    gyro_z = -((65535 - gyro_z) + 1)
    #gyro_z = gyro_z / 131.0
    return x_rot, y_rot, acc_z, gyro_x, gyro_y
 
#bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
bus = SMBus(1)
address = 0x68       # via i2cdetect
 
# Aktivieren, um das Modul ansprechen zu koennen
# Activate to be able to address the module
bus.write_byte_data(address, power_mgmt_1, 0)
bus.write_byte_data(address, 26, 3) # DLPF
print("Registre 25: {0: 08b}".format(read_byte(25))) # Sample rate divider (0=1kHz,1=500Hz... 1kHz/(1+div))
print("Registre 26: {0: 08b}".format(read_byte(26))) # DLPF config: 2=94Hz, 3=44Hz
print("Registre 27: {0: 08b}".format(read_byte(27)))
print("Registre 28: {0: 08b}".format(read_byte(28)))


K = 0.98
K1 = 1 - K


nomDuFichier = '/mesures/mesures.csv'

#Dessin de la zone graphique
largeur = 800
hauteur = 800
win = GraphWin("Angle de la planche", largeur, hauteur)
#win.yUp()
pt = Point(largeur/2, hauteur/2)
cir0 = Circle(pt, largeur*15/90)
cir0.setOutline("yellow")
cir0.draw(win)
cir1 = Circle(pt, largeur*5/90)
cir1.setOutline("green")
cir1.draw(win)
linh = Line(Point(largeur/2, hauteur-30), Point(largeur/2, 30))
linh.draw(win)
linv = Line(Point(30, hauteur/2), Point(largeur-30, hauteur/2))
linv.draw(win)
cir = Circle(pt, 8)
cir.setFill("green")
#cir.setOutline("yellow")
#cir.setWidth(2)
cir.draw(win)

#label = Text(Point(100, 120), 'Du texte')
#label.draw(win)

message = Text(Point(win.getWidth()/2, 10), "Click n'importe où pour terminer")
message.draw(win)
#win.getMouse()


x_rotation, y_rotation,accel_zout,x_gyro,y_gyro = lit_tout_MPU6050(address)
print("Avant tout: X={0:4.1f} deg, Y={1:4.1f} deg, z={2:4.1f} g, gyro_X={3:4.1f}, gyro_Y={4:4.1f}".format(x_rotation, y_rotation,accel_zout,x_gyro,y_gyro))

print("Départ: z={0:4.1f}".format(accel_zout))
print("Angle de rotation X,Y")
print("---------------------")

fichierData = open(nomDuFichier, 'w')

# Coordonnées de départ au centre
x_prec = 0
y_prec = 0
gain = largeur/90 # 90degrés font la pleine largeur d'affichage

now = time.time()
x_rotation, y_rotation, accel_zout, x_gyro, y_gyro = lit_tout_MPU6050(address)
angle_x_filtre = x_rotation
angle_y_filtre = y_rotation
gyro_offset_x = x_gyro
gyro_offset_y = y_gyro
gyro_total_x = (angle_x_filtre) - gyro_offset_x
gyro_total_y = (angle_y_filtre) - gyro_offset_y

next_t = dt

pause = next_t-(time.time()-now)
if (pause>0):
    time.sleep(pause)

clickPoint = win.checkMouse()
while (clickPoint == None):
    t = time.time()-now
    x_rotation, y_rotation, accel_zout, x_gyro, y_gyro = lit_tout_MPU6050(address)

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

    clickPoint = win.checkMouse()

    next_t = next_t + dt
    pause = next_t-(time.time()-now)
    if (pause>0):
        time.sleep(pause)

fichierData.close()
print("Les mesures sont dans ", nomDuFichier)

win.close()

print(clickPoint)

# On relie le fichier
fichierData = open(nomDuFichier, 'r')
temps = []
angleX = []
angleY = []
accX = []
accY = []
gyroX = []
gyroY = []

#uneligne = fichierData.readline()
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

# On produit les graphiques d'intérêt
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
#plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
plt.grid(True)
plt.subplot(223)
plt.plot(temps,angleY)
plt.xlabel('temps [sec]')
plt.ylabel('angle Y [deg]')
plt.grid(True)
plt.subplot(224)
plt.hist(angleY, 50, density=1, facecolor='g', alpha=0.75)
plt.xlabel('angle Y [deg]')
#plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
plt.title("$\mu_y$={0:4.1f}$^\circ$, $\sigma_y$={1:4.1f}$^\circ$".format(np.mean(angleY),np.std(angleY)))
plt.grid(True)
#plt.show()

# On produit les graphiques d'ingénierie
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

