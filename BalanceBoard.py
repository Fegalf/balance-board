import pygame
from pygame import gfxdraw
import matplotlib.pyplot as plt
import numpy as np
import time

from mpu6050_interface import MPU6050

class Timer:
    def __init__(self, seconds):
        self.seconds = seconds
        self.t_start = pygame.time.get_ticks()
        self.t_end = self.t_start + int(self.seconds*1000)

    def reset(self):
        self.t_start = pygame.time.get_ticks()
        self.t_end = self.t_start + int(self.seconds*1000)

    def is_over(self):
        return self.t_end < pygame.time.get_ticks()

    def get_remaining_time(self):
        return (self.t_end - pygame.time.get_ticks()) // 1000 + 1

class EmptyCircle:
    def __init__(self, x, y, radius, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def cursor_is_inside(self, cursor):
        # Get mouse position.
        cursor_x, cursor_y = cursor.get_position()

        # Compute circle range.
        r = np.sqrt((cursor_x - self.x) ** 2 + (cursor_y - self.y) ** 2)

        return r < self.radius

    def draw(self, display):
        # Anti alisied circles (might break in futur pygame update)
        # If so, just replace these 3 lines by:
        # pygame.draw.circle(display, self.color, (self.x, self.y), self.radius, 2).
        pygame.gfxdraw.aacircle(display, self.x, self.y, self.radius, self.color)
        pygame.gfxdraw.aacircle(display, self.x, self.y, self.radius-1, self.color)
        pygame.gfxdraw.aacircle(display, self.x, self.y, self.radius - 2, self.color)

    def update_radius(self, new_radius):
        self.radius = new_radius

class Text:
    def __init__(self, text, x, y, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.color = color

        pygame.font.init()
        self.myfont = pygame.font.SysFont('elephant', 80)
        self.textsurface = self.myfont.render(text, True, self.color)
        
    def change_text(self, text):
        self.textsurface = self.myfont.render(text, True, self.color)

    def draw(self, display, x, y):
        display.blit(self.textsurface, (x, y))

    def hide(self,):
        self.change_text("")

class Cursor:
    def __init__(self, big_circle_r, x_center, y_center, cursor_r, color=(0, 0, 0)):
        self.color = color
        self.x = x_center
        self.y = y_center
        
        self.x_center = x_center
        self.y_center = y_center
        self.gain = 6*big_circle_r / 90
        self.mpu6050 = MPU6050()

        x_rotation, y_rotation, accel_zout, x_gyro, y_gyro = self.mpu6050.read_data()
        self.angle_x_filtre = x_rotation
        self.angle_y_filtre = y_rotation
        self.gyro_offset_x = x_gyro
        self.gyro_offset_y = y_gyro
        self.gyro_total_x = (self.angle_x_filtre) - self.gyro_offset_x
        self.gyro_total_y = (self.angle_y_filtre) - self.gyro_offset_y

        self.dt = 0.01
        self.K = 0.945
        self.K1 = 1 - self.K

    def update_position(self,):
        x_rotation, y_rotation, _, x_gyro, y_gyro = self.mpu6050.read_data()
        self.x_rotation = x_rotation
        self.y_rotation = y_rotation
        
        gyro_x_delta = self.dt*(x_gyro - self.gyro_offset_x)
        gyro_y_delta = self.dt*(y_gyro - self.gyro_offset_y)

        self.gyro_total_x += gyro_x_delta
        self.gyro_total_y += gyro_y_delta
        
        self.angle_x_filtre = self.K * (self.angle_x_filtre + gyro_x_delta) + (self.K1 * x_rotation)
        self.angle_y_filtre = self.K * (self.angle_y_filtre + gyro_y_delta) + (self.K1 * y_rotation)
        
        # Updating pixel values and averaging with previous value (smoother).
        self.x = int((self.x + self.x_center + self.gain * self.angle_x_filtre)//2)
        self.y = int((self.y + self.y_center + self.gain * self.angle_y_filtre)//2)
        
    def draw(self, display):
        pygame.draw.circle(display, self.color, self.get_position(), 6)
        
    def get_position(self,):
        self.update_position()
        return self.x, self.y

class DataFile:
    def __init__(self, path_to_csv_file):
        self.f = open(path_to_csv_file, 'w')
        self.t0 = time.time()
    
        self.f.write("{0:}, {1:}, {2:}, {3:}, {4:}, "
                     "{5:}, {6:}\n".format('time',
                                                   'x_rotation',
                                                   'y_rotation',
                                                   'gyro_total_x',
                                                   'gyro_total_y',
                                                   'angle_x',
                                                   'angle_y'))
        
    def __exit__(self,):
        self.f.close()
        
    def record_mpu6050_data(self, cursor):
        t = time.time() - self.t0
        self.f.write("{0:10f}, {1:4.1f}, {2:4.1f}, {3:4.1f}, {4:4.1f}, "
                      "{5:4.1f}, {6:4.1f}\n".format(t, cursor.x_rotation,
                                                    cursor.y_rotation,
                                                    cursor.gyro_total_x,
                                                    cursor.gyro_total_y,
                                                    cursor.angle_x_filtre,
                                                    cursor.angle_y_filtre))
        

def plot_session_graphs(path_to_file):
    fichierData = open(path_to_file, 'r')
    time = []
    angleX = []
    angleY = []
    accX = []
    accY = []
    gyroX = []
    gyroY = []
    
    # skip headers line.
    next(fichierData)
    
    for x in fichierData:
      ledata = [float(y) for y in x.split(', ')]
      time.append(ledata[0])
      accX.append(ledata[1])
      accY.append(ledata[2])
      gyroX.append(ledata[3])
      gyroY.append(ledata[4])
      angleX.append(ledata[5])
      angleY.append(ledata[6])

    fichierData.close()

    plt.figure(1)  
    plt.subplot(221)
    plt.plot(time, angleX)
    plt.xlabel('time [sec]')
    plt.ylabel('angle X [deg]')
    plt.grid(True)
    plt.subplot(222)
    plt.hist(angleX, 50, density=1, facecolor='g', alpha=0.75)
    plt.xlabel('angle X [deg]')
    plt.title("$\mu_x$={0:4.1f}$^\circ$, $\sigma_x$={1:4.1f}$^\circ$".format(np.mean(angleX), np.std(angleX)))
    #plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
    plt.grid(True)
    plt.subplot(223)
    plt.plot(time,angleY)
    plt.xlabel('time [sec]')
    plt.ylabel('angle Y [deg]')
    plt.grid(True)
    plt.subplot(224)
    plt.hist(angleY, 50, density=1, facecolor='g', alpha=0.75)
    plt.xlabel('angle Y [deg]')
    #plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
    plt.title("$\mu_y$={0:4.1f}$^\circ$, $\sigma_y$={1:4.1f}$^\circ$".format(np.mean(angleY),np.std(angleY)))
    plt.grid(True)
    #plt.show()

    plt.figure(2)
    plt.subplot(211)
    plt.plot(time, angleX, time, gyroX, time, accX)
    plt.xlabel('time [sec]')
    plt.ylabel('angle X [deg]')
    plt.grid(True)
    plt.title('Les angles')
    plt.subplot(212)
    plt.plot(time, angleY, time, gyroY, time, accY)
    plt.xlabel('time [sec]')
    plt.ylabel('angle Y [deg]')
    plt.grid(True)
    plt.show()


def display_congrats(display, bg_color, text_color):
    myfont = pygame.font.SysFont('elephant', 70)
    display.fill(bg_color)
    textsurface = myfont.render("Félicitations!", True, text_color)
    
    x_center, y_center = pygame.display.get_surface().get_size()
    display.blit(textsurface, (x_center//2- 150, y_center//2 - 70))
    pygame.display.update()
    pygame.time.delay(4000)

