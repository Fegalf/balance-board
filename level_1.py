# -*- coding: utf-8 -*-

import pygame
import os
from BalanceBoard import Timer, EmptyCircle, Text, Cursor, DataFile, plot_session_graphs, display_congrats, time
from color_scheme import *

def level_1(path_to_data_folder, calibration):
    ################### LEVEL PARAMETERS ###################
    BIG_CIRCLE_RADIUS = 150 # in pixels.
    TIME_BETWEEN_DIFFICULTY_CHANGES = 10  # in seconds.
    GAIN_OF_MPU6050 = 10  # arbitrary value (test for other gain values).
    N_DIFFICULTY_LEVELS = 9
    ########################################################

    # Initialize circles radiuses (in pixels).
    big_circle_r = BIG_CIRCLE_RADIUS
    small_circle_r = int(big_circle_r - 0.1*big_circle_r)

    # Set time between difficulty changes (default: 10 seconds).
    timer_length = TIME_BETWEEN_DIFFICULTY_CHANGES

    # Number of difficulty levels.
    n_difficulty_levels = N_DIFFICULTY_LEVELS

    # Init top window in full screen.
    pygame.init()
    display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Balance Board")

    # Get width and height of display.
    size_x, size_y = pygame.display.get_surface().get_size()

    # Find center of display.
    x_center, y_center = (size_x//2, size_y//2)

    # Create circles and start timer.
    big_circle = EmptyCircle(x_center, y_center, big_circle_r)
    small_circle = EmptyCircle(x_center, y_center, small_circle_r)
    timer_10s = Timer(timer_length)

    # Initialize MPU6050 cursor.
    cursor = Cursor(GAIN_OF_MPU6050, cursor_r=7, calibration=calibration)

    # Font parameters and text initialization.
    text_timer = Text('')
    text_acq = Text("Appuyer sur ESPACE pour démarrer l'acquisition")

    # Initialize mesures file.
    data = DataFile(path_to_data_folder, game_id=1)

    t0 = time.time()
    dt = 0.023    # a verifier quelle est la frequence d'echantillonage
    next_t = dt

    # Starting game.
    difficulty = 1
    bg_color = RED
    run = True
    acquisition_started = False
    while run:
        pygame.mouse.set_visible(False)
        #pygame.time.delay(10)
        t = time.time() - t0
        cursor.update_position()
        # Exit game if "escape" or window's "X" are pressed.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # peu peut-etre etre enlevé
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

        # If cursor is outside BIG circle, background is RED.
        # If cursor in inside between SMALL and BIG circles, background is ORANGE. 
        # If cursor in inside SMALL circle, background is GREEN and timer starts.

        if acquisition_started:
            if big_circle.cursor_is_inside(cursor):
                if not small_circle.cursor_is_inside(cursor):
                    bg_color = ORANGE
                    timer_10s.reset()
                    text_timer.hide()

                else:
                    bg_color = GREEN
                    remaining_time = str(timer_10s.get_remaining_time())
                    text_timer.change_text(remaining_time)

            else:
                bg_color = RED
                timer_10s.reset()
                text_timer.hide()

            if timer_10s.is_over():
                difficulty += 1
                if difficulty == n_difficulty_levels:
                    display_congrats(display, bg_color, WHITE)
                    run = False
                    break
                new_radius = small_circle_r - int((difficulty / 10) * big_circle_r)
                small_circle.update_radius(new_radius)
                timer_10s.reset()
        else:
            timer_10s.reset()

        # Draw background and circles.
        display.fill(bg_color)
        big_circle.draw(display)
        small_circle.draw(display)

        # Draw timer.
        text_timer.draw(display, x_center - 30, 75)

        # Draw cursor.
        cursor.draw(display)
        
        # Record data. 
        if acquisition_started:
            data.record_mpu6050_data(t, cursor, difficulty)
        else:
            text_acq.draw(display, x_center//2, 40)
        pygame.display.update()
        
        next_t = next_t + dt
        pause = next_t - (time.time()-t0)
        if (pause>0):
            time.sleep(pause)

    # Plots of various measures.
    pygame.quit()
    plot_session_graphs(data.path_to_csv_file, game_id=1)
    