from BalanceBoard import *

# Initialize circles radiuses (in pixels).
cursor_r = 5
big_circle_r = 150
small_circle_r = int(big_circle_r - 0.1*big_circle_r)

# Set time between difficulty changes (defaults = 10 seconds).
timer_length = 2

# Number of difficulty levels.
n_difficulty_levels = 9

# Colors in RGB.
green = (22, 100, 27)
orange = (115, 100, 22)
red = (150, 25, 25)
black = (0, 0, 0)
white = (255, 255, 255)

cursor_color = black
timer_color = white
big_circle_color = white
small_circle_color = white

# Init top window in full screen.
pygame.init()
display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Balance Board")

# Get width and height of display.
size_x, size_y = pygame.display.get_surface().get_size()

# Find center of display.
x_center, y_center = (size_x//2, size_y//2)

# Create circles and start timer.
big_circle = EmptyCircle(x_center, y_center, big_circle_r, big_circle_color)
small_circle = EmptyCircle(x_center, y_center, small_circle_r, small_circle_color)
timer_10s = Timer(timer_length)

# Font parameters and text initialization.

text_timer = Text('', 0, 0, timer_color)

# Start coordinates of MPU6050.
cursor = Cursor(big_circle_r, x_center, y_center, cursor_r, cursor_color)

# Initialize mesures file.
path_to_mesures = 'mesures.csv'
data = DataFile(path_to_mesures)

# Starting game.
difficulty = 1
bg_color = red
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

    if big_circle.cursor_is_inside(cursor):
        if not small_circle.cursor_is_inside(cursor):
            bg_color = orange
            timer_10s.reset()
            text_timer.hide()

        else:
            bg_color = green
            remaining_time = str(timer_10s.get_remaining_time())
            text_timer.change_text(remaining_time)

    else:
        bg_color = red
        timer_10s.reset()
        text_timer.hide()

    if timer_10s.is_over():
        difficulty += 1
        if difficulty == n_difficulty_levels:
            display_congrats(display, bg_color, white)
            run = False
            break
        new_radius = small_circle_r - int((difficulty / 10) * big_circle_r)
        small_circle.update_radius(new_radius)
        timer_10s.reset()

    # Draw background and circles.
    display.fill(bg_color)
    big_circle.draw(display)
    small_circle.draw(display)

    # Draw text.
    text_timer.draw(display, x_center - 30, 75)

    # Get position of the cursor and draw a red circle on it.
    cursor.draw(display)
    
    data.record_mpu6050_data(cursor)
    pygame.display.update()
    
pygame.quit()

plot_session_graphs(path_to_mesures)