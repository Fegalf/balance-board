# -*- coding: utf-8 -*-

import pygame
import time
import math
from color_scheme import GREEN, ORANGE, RED, BLACK, WHITE, GREY
from BalanceBoard import Timer, EmptyCircle, Text, Cursor, DataFile, \
                         plot_session_graphs, display_congrats, \
                         point_inside_polygon, Course, DistanceLine

# Init top window in full screen.
pygame.init()
display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Balance Board")

# Find height of display.
height = pygame.display.get_surface().get_size()[1]

############################## LEVELS PARAMETERS ##############################

START_CIRCLE_RADIUS = 30
TIME_BETWEEN_SUBLEVELS_CHANGES = 5

GAIN_OF_MPU6050 = 10  # Gain values should be calibrated using the balance board (trials and errors).
NUMBER_OF_TRIAL = 3

# Each line represents a sublevel's angle, distance from the screen's center, radius of starting circle and radius of end circle.
SUBLEVELS = [(90, START_CIRCLE_RADIUS),
          (180, START_CIRCLE_RADIUS),
          (0,  START_CIRCLE_RADIUS),
          (135, START_CIRCLE_RADIUS),
          (45, START_CIRCLE_RADIUS),
          (270, START_CIRCLE_RADIUS),]

###################################################################################

# Set time between sublevel changes (default: 3 seconds).
timer_length = TIME_BETWEEN_SUBLEVELS_CHANGES

# Setting up different levels of difficulty.
number_of_trial = NUMBER_OF_TRIAL
sublvl_index = 0
max_distance_reached = 0
course = Course(*SUBLEVELS[sublvl_index], max_distance_reached)

# Font parameters and text initialization.
text_timer = Text('', 0, 0)
text_lvl = Text('', 0, 0)
text_lvl.change_text(str(sublvl_index))

# Start coordinates of MPU6050.
cursor = Cursor(GAIN_OF_MPU6050) 

# Initialize mesures file.
path_to_mesures = 'mesures.csv'
data = DataFile(path_to_mesures)

#Timer
timer = Timer(timer_length)

# Starting game.
n_try = 0
bg_color = ORANGE
run = True
 

t0 = time.time()
dt = 0.023    # a verifier quelle est la frequence d'echantillonage
next_t = dt
display.fill(bg_color)
just_finished = False

while run:
    pygame.mouse.set_visible(False)
    t = time.time() - t0
    cursor.update_position()
    y_pos = height//2 - cursor.get_position()[1]

    if y_pos > max_distance_reached:
        max_distance_reached = y_pos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    if course.cursor_inside_start_circle(cursor):
        bg_color = ORANGE
        if not just_finished:
            bg_color = GREEN
            remaining_time = str(timer.get_remaining_time())
            text_timer.change_text(remaining_time)
            course.update_colors(bg_color)

    else:
        just_finished = False
        bg_color = ORANGE
        course.update_colors(bg_color)
        timer.reset()
        text_timer.hide()

    if timer.is_over():
        if n_try < (NUMBER_OF_TRIAL-1):
            n_try += 1
        else:
            sublvl_index += 1
            max_distance_reached = 0
            text_lvl.change_text(str(sublvl_index))
            if sublvl_index == len(SUBLEVELS):
                display_congrats(display, bg_color, WHITE)
                run = False
                break
        just_finished = True
        new_distance = max_distance_reached
        course = Course(*SUBLEVELS[sublvl_index], new_distance)
        timer.reset()
    
    # Draw text.
    display.fill(bg_color)
    text_timer.draw(display, 100, 75)
    text_lvl.draw(display, 25, height-70)

    # Get position of the cursor and draw a red circle on it.
    course.draw(display)
    cursor.draw(display)
    pygame.display.update()

    next_t = next_t + dt
    pause = next_t - (time.time() - t0)
    if (pause>0):
        time.sleep(pause)
    data.record_mpu6050_data(t, cursor, sublvl_index)

pygame.quit()

#plot_session_graphs(path_to_mesures)
