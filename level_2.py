# -*- coding: utf-8 -*-

import pygame
import time
import numpy as np
import math
from color_scheme import GREEN, ORANGE, RED, BLACK, WHITE, GREY
from BalanceBoard import Timer, EmptyCircle, Text, Cursor, DataFile, \
                         plot_session_graphs, display_congrats, \
                         point_inside_polygon, Course, DistanceLine, get_center_of_display

def level_2(path_to_data_folder, calibration):
    # Init top window in full screen.
    pygame.init()
    display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Balance Board")

    # Get width and height of display.
    size_x, height = pygame.display.get_surface().get_size()

    # Find center of display.
    x_center, y_center = (size_x//2, height//2)

    ############################## LEVELS PARAMETERS ##############################

    START_CIRCLE_RADIUS = 30
    TIME_BETWEEN_SUBLEVELS_CHANGES = 2

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
    text_timer = Text('')
    text_lvl = Text('')
    text_lvl.change_text(str(sublvl_index))
    text_acq = Text("Appuyer sur ESPACE pour démarrer l'acquisition")

    # Start coordinates of MPU6050.
    cursor = Cursor(GAIN_OF_MPU6050, calibration=calibration) 

    # Initialize mesures file.
    data = DataFile(path_to_data_folder, game_id=2)

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
    just_finished = True
    acquisition_started = False

    def get_projection_on_path(cursor, angle_of_path):
        x, y = cursor.get_position()
        xc, yc = get_center_of_display()
        L = np.sqrt((x - xc)**2 + (yc - y)**2 )
        theta = np.radians(angle_of_path)

        try:
            alpha = np.arctan2((yc - y), (x - xc))
            sin_theta, cos_theta = np.sin(theta), np.cos(theta)
            sin_alpha, cos_alpha = np.sin(alpha), np.cos(alpha)
            p = L * (cos_alpha * cos_theta + sin_theta * sin_alpha) 

        except:
            p = 0
        return p

    while run:
        pygame.mouse.set_visible(False)
        t = time.time() - t0
        cursor.update_position()
        angle_of_path = SUBLEVELS[sublvl_index][0]

        if acquisition_started:
            d = get_projection_on_path(cursor, angle_of_path)

            if d > max_distance_reached:
                max_distance_reached = d
        else:
            d = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if (event.key == pygame.K_SPACE) or (event.key == pygame.K_RETURN):
                    if not acquisition_started:
                        t0 = time.time()
                        t = 0
                        next_t = 0
                    acquisition_started = True

        if acquisition_started:
            if course.cursor_inside_start_circle(cursor):
                bg_color = ORANGE
                if not just_finished:
                    bg_color = GREEN
                    remaining_time = str(timer.get_remaining_time())
                    text_timer.change_text(remaining_time)
                    course.update_colors(bg_color)

                else:
                    timer.reset()

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
                    n_try = 0 
                    if sublvl_index == len(SUBLEVELS):
                        display_congrats(display, bg_color, WHITE)
                        run = False
                        break
                just_finished = True
                new_distance = max_distance_reached
                course = Course(*SUBLEVELS[sublvl_index], new_distance)
                timer.reset()
        else:
            timer.reset()
            

        # Draw text.
        display.fill(bg_color)
        text_timer.draw(display, 100, 75)
        text_lvl.draw(display, 25, height-70)
        if not acquisition_started:
            text_acq.draw(display, x_center//2, 40)

        # Get position of the cursor and draw a red circle on it.
        course.draw(display)
        cursor.draw(display, draw_trail=True)
        pygame.display.update()

        next_t = next_t + dt
        pause = next_t - (time.time() - t0) 
        if (pause>0):
            time.sleep(pause)
        if acquisition_started:
            data.record_mpu6050_data(t, cursor, sublvl_index, n_try)

    pygame.quit()
    plot_session_graphs(data.path_to_csv_file, game_id=2)
