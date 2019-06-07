import pygame
from colors import GREEN, ORANGE, RED, BLACK, WHITE
from BalanceBoard import Timer, EmptyCircle, Text, Cursor, DataFile, \
                         plot_session_graphs, display_congrats, \
                         point_inside_polygon, Mouse, Course

# Initialize circles radiuses (in pixels).
cursor_r = 5
big_circle_r = 30

# Set time between difficulty changes (defaults = 10 seconds).
timer_length = 3

# Colors of elements.
cursor_color = BLACK
timer_color = WHITE
big_circle_color = WHITE

# Init top window in full screen.
pygame.init()
display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Balance Board")

# Find height of display.
height = pygame.display.get_surface().get_size()[1]

# Setting up different levels of difficulty.
max_number_of_fails = 4
start_circle_r = 30

big_circle = 90
medium_circle = 60
small_circle = 30

levels = [(90, height // 6, start_circle_r, big_circle),
          (180, height // 6, start_circle_r, big_circle),
          (0, height // 6, start_circle_r, big_circle),
          (135, height // 6, start_circle_r, big_circle),
          (45, height // 6, start_circle_r, big_circle),
          (270, height // 6, start_circle_r, big_circle),
          (90, height // 5, start_circle_r, big_circle),
          (180, height // 5, start_circle_r, big_circle),
          (0, height // 5, start_circle_r, big_circle),
          (135, height // 5, start_circle_r, big_circle),
          (45, height // 5, start_circle_r, big_circle),
          (270, height // 5, start_circle_r, big_circle),
          (90, height // 3, start_circle_r, big_circle),
          (180, height // 3, start_circle_r, big_circle),
          (0, height // 3, start_circle_r, big_circle),
          (135, height // 3, start_circle_r, big_circle),
          (45, height // 3, start_circle_r, big_circle),
          (270, height // 3, start_circle_r, big_circle),
          (90, height // 6, start_circle_r, medium_circle),
          (180, height // 6, start_circle_r, medium_circle),
          (0, height // 6, start_circle_r, medium_circle),
          (135, height // 6, start_circle_r, medium_circle),
          (45, height // 6, start_circle_r, medium_circle),
          (270, height // 6, start_circle_r, medium_circle),
          (90, height // 5, start_circle_r, medium_circle),
          (180, height // 5, start_circle_r, medium_circle),
          (0, height // 5, start_circle_r, medium_circle),
          (135, height // 5, start_circle_r, medium_circle),
          (45, height // 5, start_circle_r, medium_circle),
          (270, height // 5, start_circle_r, medium_circle),
          (90, height // 3, start_circle_r, medium_circle),
          (180, height // 3, start_circle_r, medium_circle),
          (0, height // 3, start_circle_r, medium_circle),
          (135, height // 3, start_circle_r, medium_circle),
          (45, height // 3, start_circle_r, medium_circle),
          (270, height // 3, start_circle_r, medium_circle),
          (90, height // 6, start_circle_r, small_circle),
          (180, height // 6, start_circle_r, small_circle),
          (0, height // 6, start_circle_r, small_circle),
          (135, height // 6, start_circle_r, small_circle),
          (45, height // 6, start_circle_r, small_circle),
          (270, height // 6, start_circle_r, small_circle),
          (90, height // 5, start_circle_r, small_circle),
          (180, height // 5, start_circle_r, small_circle),
          (0, height // 5, start_circle_r, small_circle),
          (135, height // 5, start_circle_r, small_circle),
          (45, height // 5, start_circle_r, small_circle),
          (270, height // 5, start_circle_r, small_circle),
          (90, height // 3, start_circle_r, small_circle),
          (180, height // 3, start_circle_r, small_circle),
          (0, height // 3, start_circle_r, small_circle),
          (135, height // 3, start_circle_r, small_circle),
          (45, height // 3, start_circle_r, small_circle),
          (270, height // 3, start_circle_r, small_circle)]

lvl_index = 0
course = Course(*levels[lvl_index])

# Font parameters and text initialization.
text_timer = Text('', 0, 0, timer_color)

# Start coordinates of MPU6050.
cursor = Cursor(big_circle_r, cursor_r, cursor_color)

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
                    course = Course(*levels[lvl_index])
                    n_fail = 0
                except IndexError:
                    display_congrats(display, bg_color, white)
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
            course = Course(*levels[lvl_index])
            bg_color = RED
            course.update_colors(RED, RED, RED)
            failed = True
            timer.reset()
            text_timer.hide()

    # Draw background and circles.
    display.fill(bg_color)
    course.draw(display)

    # Draw text.
    text_timer.draw(display, 100, 75)

    # Get position of the cursor and draw a red circle on it.
    cursor.draw(display)
    data.record_mpu6050_data(cursor)
    pygame.display.update()

    prev_failed = failed

pygame.quit()

#plot_session_graphs(path_to_mesures)