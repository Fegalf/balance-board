#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import time
import math
from color_scheme import GREEN, ORANGE, RED, BLACK, WHITE
from BalanceBoard import Timer, EmptyCircle, Text, Cursor, DataFile, \
                         plot_session_graphs, display_congrats, \
                         point_inside_polygon, Mouse, Course

# Init top window in full screen.
pygame.init()
display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Balance Board")

# Find height of display.
height = pygame.display.get_surface().get_size()[1]

############################## LEVELS PARAMETERS ##############################

START_CIRCLE_RADIUS = 30
END_CIRCLE_RADIUS_easy = 90
END_CIRCLE_RADIUS_medium = 60
END_CIRCLE_RADIUS_hard = 30

TIME_BETWEEN_SUBLEVELS_CHANGES = 3
GAIN_OF_MPU6050 = 10  # Gain values should be calibrated using the balance board (trials and errors).
MAXIMUM_NUMBER_OF_FAILS = 3

# Each line represents a sublevel's angle, distance from the screen's center, radius of starting circle and radius of end circle.
SUBLEVELS = [(90, height // 6, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_easy),
          (180, height // 6, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_easy),
          (0, height // 6, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_easy),
          (135, height // 6, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_easy),
          (45, height // 6, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_easy),
          (270, height // 6, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_easy),
          (90, height // 5, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_easy),
          (180, height // 5, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_easy),
          (0, height // 5, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_easy),
          (135, height // 5, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_easy),
          (45, height // 5, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_easy),
          (270, height // 5, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_easy),
          (90, height // 3, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_easy),
          (180, height // 3, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_easy),
          (0, height // 3, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_easy),
          (135, height // 3, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_easy),
          (45, height // 3, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_easy),
          (270, height // 3, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_easy),
          (90, height // 6, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_medium),
          (180, height // 6, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_medium),
          (0, height // 6, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_medium),
          (135, height // 6, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_medium),
          (45, height // 6, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_medium),
          (270, height // 6, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_medium),
          (90, height // 5, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_medium),
          (180, height // 5, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_medium),
          (0, height // 5, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_medium),
          (135, height // 5, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_medium),
          (45, height // 5, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_medium),
          (270, height // 5, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_medium),
          (90, height // 3, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_medium),
          (180, height // 3, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_medium),
          (0, height // 3, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_medium),
          (135, height // 3, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_medium),
          (45, height // 3, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_medium),
          (270, height // 3, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_medium),
          (90, height // 6, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_hard),
          (180, height // 6, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_hard),
          (0, height // 6, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_hard),
          (135, height // 6, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_hard),
          (45, height // 6, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_hard),
          (270, height // 6, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_hard),
          (90, height // 5, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_hard),
          (180, height // 5, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_hard),
          (0, height // 5, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_hard),
          (135, height // 5, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_hard),
          (45, height // 5, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_hard),
          (270, height // 5, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_hard),
          (90, height // 3, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_hard),
          (180, height // 3, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_hard),
          (0, height // 3, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_hard),
          (135, height // 3, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_hard),
          (45, height // 3, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_hard),
          (270, height // 3, START_CIRCLE_RADIUS, END_CIRCLE_RADIUS_hard)]

###################################################################################

# Set time between sublevel changes (default: 3 seconds).
timer_length = TIME_BETWEEN_SUBLEVELS_CHANGES

# Setting up different levels of difficulty.
max_number_of_fails = MAXIMUM_NUMBER_OF_FAILS
lvl_index = 0
course = Course(*SUBLEVELS[lvl_index])

# Font parameters and text initialization.
text_timer = Text('', 0, 0)
text_lvl = Text('', 0, 0)
text_lvl.change_text(str(lvl_index))

# Start coordinates of MPU6050.
cursor = Cursor(GAIN_OF_MPU6050) 


# Initialize mesures file.
path_to_mesures = 'mesures.csv'
data = DataFile(path_to_mesures)

#Timer
timer = Timer(timer_length)

# Starting game.
n_fail = 0
prev_failed = False
failed = False
bg_color = GREEN
run = True
distance_reached = 0 

t0 = time.time()
dt = 0.023    # a verifier quelle est la frequence d'echantillonage
next_t = dt
display.fill(bg_color)

while run:
    pygame.mouse.set_visible(False)
    t = time.time() - t0
    cursor.update_position()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    if course.cursor_inside_start_circle(cursor):
        bg_color = ORANGE
        course.update_colors(ORANGE, ORANGE, ORANGE)
        failed = False
        timer.reset()
        text_timer.hide()
    
    y_pos = cursor.get_position()[1]
    if y_pos > distance_reached:
        distance_reached = y_pos

    # Draw background and circles.
    
    course.draw(display)

    # Draw text.
    text_timer.draw(display, 100, 75)
    text_lvl.draw(display, 25, height-70)

    # Get position of the cursor and draw a red circle on it.
    cursor.draw(display)
    pygame.display.update()

    next_t = next_t + dt
    pause = next_t - (time.time() - t0)
    if (pause>0):
        time.sleep(pause)
    data.record_mpu6050_data(t, cursor, lvl_index)

pygame.quit()

plot_session_graphs(path_to_mesures)
