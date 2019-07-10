#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
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
bg_color = RED
run = True
while run:
    pygame.mouse.set_visible(False)
    pygame.time.delay(10)
    
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

    if not failed:
        if course.cursor_inside_end_circle(cursor):
            bg_color = GREEN
            course.update_colors(GREEN, GREEN, GREEN)
            remaining_time = str(timer.get_remaining_time())
            text_timer.change_text(remaining_time)

            if timer.is_over():
                try:
                    lvl_index += 1
                    course = Course(*SUBLEVELS[lvl_index])
                    n_fail = -1
                    text_lvl.change_text(str(lvl_index))
                except IndexError:
                    display_congrats(display, bg_color)
                    run = False
                    break

                timer.reset()
                text_timer.hide()

        elif course.cursor_inside_trail(cursor) or course.cursor_inside_start_circle(cursor):
            bg_color = ORANGE
            course.update_colors(ORANGE, ORANGE, ORANGE)
            timer.reset()
            text_timer.hide()

        else:
            bg_color = RED
            course.update_colors(RED, RED, RED)
            failed = True

            timer.reset()
            text_timer.hide()

    if failed:
        if not prev_failed:
            if lvl_index != 0:
                n_fail += 1

        if (n_fail == max_number_of_fails) and (lvl_index != 0):
            lvl_index -= 1
            n_fail = 0
            course = Course(*SUBLEVELS[lvl_index])
            bg_color = RED
            course.update_colors(RED, RED, RED)
            failed = True
            timer.reset()
            text_timer.hide()
            text_lvl.change_text(str(lvl_index))

    # Draw background and circles.
    display.fill(bg_color)
    course.draw(display)

    # Draw text.
    text_timer.draw(display, 100, 75)
    text_lvl.draw(display, 25, height-70)

    # Get position of the cursor and draw a red circle on it.
    cursor.draw(display)
    data.record_mpu6050_data(cursor,lvl_index)

    pygame.display.update()

    prev_failed = failed

pygame.quit()

plot_session_graphs(path_to_mesures)
