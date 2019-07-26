# -*- coding: utf-8 -*-

import pygame
from BalanceBoard import Timer, EmptyCircle, Text, Cursor, DataFile, plot_session_graphs, display_congrats, time
from color_scheme import *

def level_0(path_to_data_folder, calibration):
    ################### LEVEL PARAMETERS ###################
    GAIN_OF_MPU6050 = 10  # arbitrary value (test for other gain values).
    CENTER_CIRCLE_RADIUS = 30
    ########################################################

    # Initialize circles radiuses (in pixels).
    small_circle_r = CENTER_CIRCLE_RADIUS

    # Init top window in full screen.
    pygame.init()
    display = pygame.display.set_mode((0, 0))#, pygame.FULLSCREEN)
    pygame.display.set_caption("Balance Board")

    # Get width and height of display.
    size_x, size_y = pygame.display.get_surface().get_size()

    # Find center of display.
    x_center, y_center = (size_x//2, size_y//2)

    # Create circles and start timer.
    small_circle = EmptyCircle(x_center, y_center, small_circle_r)

    # Initialize MPU6050 cursor.
    cursor = Cursor(GAIN_OF_MPU6050, cursor_r=7, calibration=calibration)

    # Initialize mesures file.
    data = DataFile(path_to_data_folder, game_id=0)

    t0 = time.time()
    dt = 0.023    # a verifier quelle est la frequence d'echantillonage
    next_t = dt

    # Starting game.
    bg_color = GREEN
    run = True
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

        # Draw background and circles.
        display.fill(bg_color)
        small_circle.draw(display)

        # Draw cursor.
        cursor.draw(display)
        
        # Record data. 
        #data.record_mpu6050_data(t, cursor, difficulty)

        pygame.display.update()
        
        next_t = next_t + dt
        pause = next_t - (time.time()-t0)
        if (pause>0):
            time.sleep(pause)

    # Plots of various measures.
    #plot_session_graphs(data.path_to_csv_file)
    pygame.quit()