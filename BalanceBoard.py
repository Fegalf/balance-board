# -*- coding: utf-8 -*-

import pygame
import matplotlib.pyplot as plt
import numpy as np
import time
from pygame import gfxdraw
from color_scheme import GREEN, ORANGE, RED, BLACK, WHITE
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

class DistanceLine:
    def __init__(self, distance, angle, x_center, y_center, color):
        #TODO: REPLACE CIRCLE BY TRIANGLE 
        # angle in radians.
        self.distance
        self.angle
        self.start_xy = (x_center, y_center)
        self.end_xy = self.compute_line_end_xy()
        self.color = color

    def compute_line_end_xy(self):
        sin = np.sin(self.angle)
        cos = np.cos(self.angle)
        end_x = self.start_xy[0] + cos * self.distance
        end_y = self.start_xy[1] - sin * self.distance
        return end_x, end_y

    def _compute_polygon_points(self, x_center, y_center):
        points = []

        sin = np.sin(self.angle)
        cos = np.cos(self.angle)
        sin0 = np.sin(self.angle - np.pi/2)
        cos0 = np.cos(self.angle - np.pi/2)

        p0_x = int(x_center + self.distance * cos0)
        p0_y = int(y_center + self.distance * sin0)
        points.append((p0_x, p0_y))

        p1_x = int(x_center - self.distance * cos0)
        p1_y = int(y_center - self.distance * sin0)
        points.append((p1_x, p1_y))

        p2_x = int(x_center + self.distance * cos - self.distance * sin)
        p2_y = int(y_center + self.distance * sin + self.distance * cos)
        points.append((p2_x, p2_y))

        return points

    def draw(self, display):
        pygame.draw.line(display, self.color, self.start_xy, self.end_xy, 3)
        pygame.draw.circle(display, self.color, self.end_xy, 6)
 
class EmptyCircle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.R = radius
        self.color = BLACK

    def cursor_is_inside(self, cursor):
        # Get mouse position.
        cursor_x, cursor_y = cursor.get_position()

        # Compute circle range.
        r = np.sqrt((cursor_x - self.x) ** 2 + (cursor_y - self.y) ** 2)

        return r < self.R

    def draw(self, display):
        # Anti alisied circles (might break in futur pygame update)
        # If so, just replace these 2 lines by:
        pygame.draw.circle(display, self.color, (self.x, self.y), self.R, 6)
        #pygame.gfxdraw.aacircle(display, self.x, self.y, self.R, self.color)
        #pygame.gfxdraw.aacircle(display, self.x, self.y, self.R-1, self.color)

    def update_radius(self, new_radius):
        self.R = new_radius


class FilledCircle(EmptyCircle):
    def __init__(self, x, y, radius, color):
        super().__init__(x, y, radius)
        self.color = color

    def draw(self, display):
        pygame.gfxdraw.filled_circle(display, self.x, self.y, self.R, self.color)
        pygame.gfxdraw.aacircle(display, self.x, self.y, self.R, BLACK)
        pygame.gfxdraw.aacircle(display, self.x, self.y, self.R-1, BLACK)

    def update_color(self, new_color):
        self.color = new_color


class Polygon:
    def __init__(self, pointlist, color):
        self.pointlist = pointlist
        self.color = color

    def cursor_is_inside(self, cursor):
        # Get mouse position.
        cursor_x, cursor_y = cursor.get_position()
        return point_inside_polygon(cursor_x, cursor_y, self.pointlist)

    def draw(self, display):
        pygame.draw.polygon(display, self.color, self.pointlist)
        pygame.draw.polygon(display, WHITE, self.pointlist, 1)
        pygame.gfxdraw.aapolygon(display,  self.pointlist, WHITE)

    def update_color(self, new_color):
        self.color = new_color


class Course:
    def __init__(self, angle_in_degrees, start_circle_r, distance=0,
                 duration_in_seconds=5, start_circle_color=ORANGE):

        self.x_start, self.y_start = get_center_of_display()
        self.distance = distance
        self.timer = Timer(duration_in_seconds)
        self.angle_in_rads = np.radians(-angle_in_degrees)

        # colors
        self.start_circle_color = start_circle_color
        self.x_end = int(self.x_start + self.distance * np.cos(self.angle_in_rads))
        self.y_end = int(self.y_start + self.distance * np.sin(self.angle_in_rads))

        self.start_circle = FilledCircle(self.x_start, self.y_start, start_circle_r, self.start_circle_color)
        self.line = DistanceLine(self.distance, self.angle_in_rads, self.x_end, self.y_end, BLACK)

    def cursor_inside_start_circle(self, cursor):
        return self.start_circle.cursor_is_inside(cursor)

    def draw(self, display):
        self.line.draw(display)
        self.start_circle.draw(display)

    def update_colors(self, start_circle_color):
        self.start_circle.update_color(start_circle_color)


"""
class Course_old:
    #TODO: REMOVE
    def __init__(self, angle_in_degrees, length,
                 start_circle_r, end_circle_r, duration_in_seconds=3,
                 start_circle_color=ORANGE, end_circle_color=ORANGE,
                 course_color=ORANGE):

        self.x_center, self.y_center = get_center_of_display()
        self.length = length
        self.timer = Timer(duration_in_seconds)
        self.angle_in_rads = np.radians(-angle_in_degrees)

        # colors
        self.course_color = course_color
        self.start_circle_color = start_circle_color
        self.end_circle_color = end_circle_color

        x_end = int(self.x_center + length * np.cos(self.angle_in_rads))
        y_end = int(self.y_center + length * np.sin(self.angle_in_rads))

        self.start_circle = FilledCircle(self.x_center, self.y_center, start_circle_r, self.start_circle_color)
        self.end_circle = FilledCircle(x_end, y_end, end_circle_r, self.end_circle_color)
        self.polygon = Polygon(self._compute_polygon_points(self.x_center, self.y_center), self.course_color)

    def _compute_polygon_points(self, x_center, y_center):
        points = []

        sin = np.sin(self.angle_in_rads)
        cos = np.cos(self.angle_in_rads)
        sin0 = np.sin(self.angle_in_rads - np.pi/2)
        cos0 = np.cos(self.angle_in_rads - np.pi/2)

        p0_x = int(x_center + self.start_circle.R * cos0)
        p0_y = int(y_center + self.start_circle.R * sin0)
        points.append((p0_x, p0_y))

        p1_x = int(x_center - self.start_circle.R * cos0)
        p1_y = int(y_center - self.start_circle.R * sin0)
        points.append((p1_x, p1_y))

        p2_x = int(x_center + self.length * cos - self.end_circle.R * sin)
        p2_y = int(y_center + self.length * sin + self.end_circle.R * cos)
        points.append((p2_x, p2_y))

        p3_x = int(x_center + self.length * cos + self.end_circle.R * sin)
        p3_y = int(y_center + self.length * sin - self.end_circle.R * cos)
        points.append((p3_x, p3_y))
        return points

    def cursor_inside_end_circle(self, cursor):
        return self.end_circle.cursor_is_inside(cursor)

    def cursor_inside_start_circle(self, cursor):
        return self.start_circle.cursor_is_inside(cursor)

    def cursor_inside_trail(self, cursor):
        return self.polygon.cursor_is_inside(cursor)

    def draw(self, display):
        self.polygon.draw(display)
        self.start_circle.draw(display)
        self.end_circle.draw(display)

    def update_colors(self, start_circle_color, course_color, end_circle_color):
        self.start_circle.update_color(start_circle_color)
        self.polygon.update_color(course_color)
        self.end_circle.update_color(end_circle_color)
"""

class Text:
    def __init__(self, text, x, y, color=WHITE):
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
    def __init__(self, gain, cursor_r=5, color=WHITE):

        self.x_center, self.y_center = get_center_of_display()
        self.x = self.x_center
        self.y = self.y_center
        self.cursor_r = cursor_r
        self.color = color

        self.gain = gain
        self.mpu6050 = MPU6050()

        x_rotation, y_rotation, accel_zout, x_gyro, y_gyro = self.mpu6050.read_data()
        self.angle_x_filtre = x_rotation
        self.angle_y_filtre = y_rotation
        self.gyro_offset_x = x_gyro
        self.gyro_offset_y = y_gyro
        self.gyro_total_x = self.angle_x_filtre - self.gyro_offset_x
        self.gyro_total_y = self.angle_y_filtre - self.gyro_offset_y

        self.dt = 0.023
        self.K = 0.97  # etait 0.945
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
        #self.x = int((self.x + self.x_center + self.gain * self.angle_x_filtre)//2)
        #self.y = int((self.y + self.y_center + self.gain * self.angle_y_filtre)//2)
        self.x = int(self.x_center + self.gain * self.angle_x_filtre)
        self.y = int(self.y_center + self.gain * self.angle_y_filtre)
        
    def draw(self, display):
        pygame.draw.circle(display, self.color, self.get_position(), self.cursor_r)
        
    def get_position(self,):
        return self.x, self.y


class DataFile:
    def __init__(self, path_to_csv_file):
        self.f = open(path_to_csv_file, 'w')
        #self.t0 = time.time()
    
        self.f.write("{0:}, {1:}, {2:}, {3:}, {4:}, "
                     "{5:}, {6:}, {7:}\n".format('time', 'niveau',
                                                   'x_rotation',
                                                   'y_rotation',
                                                   'gyro_total_x',
                                                   'gyro_total_y',
                                                   'angle_x',
                                                   'angle_y'))
        
    def __exit__(self,):
        self.f.close()
        
    def record_mpu6050_data(self, t, cursor, niveau):
        self.f.write("{0:10f}, {1:4.1f}, {2:4.1f}, {3:4.1f}, {4:4.1f}, "
                      "{5:4.1f}, {6:4.1f}, {7:4.1f}\n".format(t, niveau,
                                                    cursor.x_rotation,
                                                    cursor.y_rotation,
                                                    cursor.gyro_total_x,
                                                    cursor.gyro_total_y,
                                                    cursor.angle_x_filtre,
                                                    cursor.angle_y_filtre))

def get_center_of_display():
    x, y = pygame.display.get_surface().get_size()
    return x//2, y//2

def plot_session_graphs(path_to_file):
    fichierData = open(path_to_file, 'r')
    temps = []
    niveau = []
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
        temps.append(ledata[0])
        niveau.append(ledata[1])
        accX.append(ledata[2])
        accY.append(ledata[3])
        gyroX.append(ledata[4])
        gyroY.append(ledata[5])
        angleX.append(ledata[6])
        angleY.append(ledata[7])

    fichierData.close()

    plt.figure(1)  
    plt.subplot(221)
    plt.plot(temps, angleX)
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
    plt.plot(temps,angleY)
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
    plt.plot(temps, angleX, temps, gyroX, temps, accX)
    plt.xlabel('time [sec]')
    plt.ylabel('angle X [deg]')
    plt.grid(True)
    plt.title('Les angles')
    plt.subplot(212)
    plt.plot(temps, angleY, temps, gyroY, temps, accY)
    plt.xlabel('time [sec]')
    plt.ylabel('angle Y [deg]')
    plt.grid(True)
    plt.show()


def display_congrats(display, bg_color, text_color=WHITE):
    myfont = pygame.font.SysFont('elephant', 70)
    display.fill(bg_color)
    textsurface = myfont.render("Félicitations!", True, text_color)
    
    x_center, y_center = pygame.display.get_surface().get_size()
    display.blit(textsurface, (x_center//2- 150, y_center//2 - 70))
    pygame.display.update()
    pygame.time.delay(4000)


def point_inside_polygon(x, y, poly, include_edges=True):
    '''
    Test if point (x,y) is inside polygon poly.

    poly is N-vertices polygon defined as
    [(x1,y1),...,(xN,yN)] or [(x1,y1),...,(xN,yN),(x1,y1)]
    (function works fine in both cases)

    Geometrical idea: point is inside polygon if horisontal beam
    to the right from point crosses polygon even number of times.
    Works fine for non-convex polygons.
    '''
    n = len(poly)
    inside = False

    p1x, p1y = poly[0]
    for i in range(1, n + 1):
        p2x, p2y = poly[i % n]
        if p1y == p2y:
            if y == p1y:
                if min(p1x, p2x) <= x <= max(p1x, p2x):
                    # point is on horisontal edge
                    inside = include_edges
                    break
                elif x < min(p1x, p2x):  # point is to the left from current edge
                    inside = not inside
        else:  # p1y!= p2y
            if min(p1y, p2y) <= y <= max(p1y, p2y):
                xinters = (y - p1y) * (p2x - p1x) / float(p2y - p1y) + p1x

                if x == xinters:  # point is right on the edge
                    inside = include_edges
                    break

                if x < xinters:  # point is to the left from current edge
                    inside = not inside

        p1x, p1y = p2x, p2y

    return inside
