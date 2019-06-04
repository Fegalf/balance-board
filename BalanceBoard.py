import pygame
from pygame import gfxdraw
import numpy as np
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

    def cursor_is_inside(self,):
        # Get mouse position.
        cursor_x, cursor_y = pygame.mouse.get_pos()

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
        self.textsurface = myfont.render(text, True, white)
        self.x = x
        self.y = y
        self.color = color

    def change_text(self, text):
        self.textsurface = myfont.render(text, True, white)

    def draw(self, display, x, y):
        display.blit(self.textsurface, (x, y))

    def hide(self,):
        self.change_text("")

class Cursor:
    def __init__(self, display_width, color=(0, 0, 0)):
        self.color = color
        self.x_prec = 0
        self.y_prec = 0
        self.gain = display_width / 90
        self.mpu6050 = MPU6050()

        x_rotation, y_rotation, accel_zout, x_gyro, y_gyro = self.mpu6050.read_data()

        self.angle_x_filtre = x_rotation
        self.angle_y_filtre = y_rotation
        self.gyro_offset_x = x_gyro
        self.gyro_offset_y = y_gyro
        self.gyro_total_x = (self.angle_x_filtre) - self.gyro_offset_x
        self.gyro_total_y = (self.angle_y_filtre) - self.gyro_offset_y

        self.dt = 0.01
        self.K = 0.98
        self.K1 = 1 - self.K

    def get_position(self,):
        x_rotation, y_rotation, accel_zout, x_gyro, y_gyro = self.mpu6050.read_data()

        gyro_x_delta = self.dt * (x_gyro - self.gyro_offset_x)
        gyro_y_delta = self.dt * (y_gyro - self.gyro_offset_y)

        self.gyro_total_x = self.gyro_total_x + gyro_x_delta
        self.gyro_total_y = self.gyro_total_y + gyro_y_delta
        self.angle_x_filtre = self.K * (self.angle_x_filtre + gyro_x_delta) + (self.K1 * x_rotation)
        self.angle_y_filtre = self.K * (self.angle_y_filtre + gyro_y_delta) + (self.K1 * y_rotation)

        x, y = self.gain * (self.angle_x_filtre - self.x_prec), self.gain * (self.angle_y_filtre - self.y_prec)
        self.x_prec = self.angle_x_filtre
        self.y_prec = self.angle_y_filtre

        return int(x), int(y)

    def draw(self, display):
        pygame.draw.circle(display, self.color, self.get_position(), 5)

def display_congrats(display):
    myfont = pygame.font.SysFont('elephant', 70)
    display.fill(bg_color)
    textsurface = myfont.render("Félicitations!", True, white)
    display.blit(textsurface, (x_pos - 150, y_pos - 70))
    pygame.display.update()
    pygame.time.delay(4000)


if __name__=="__main__":

    # Initialize mesures file.
    nomDuFichier = './mesures/mesures.csv'
    fichierData = open(nomDuFichier, 'w')

    # Initialize circles radiuses (in pixels).
    cursor_r = 5
    big_circle_r = 135
    small_circle_r = int(big_circle_r - 0.1*big_circle_r)

    # Set time between difficulty changes (defaults = 10 seconds).
    timer_length = 10

    # Colors in RGB.
    green = (22, 100, 27)
    orange = (115, 100, 22)
    red = (150, 25, 25)
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Init top window in full screen.
    pygame.init()
    display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Balance Board")

    # Get width and height of display.
    size_x, size_y = pygame.display.get_surface().get_size()

    # Find center of display.
    x_pos, y_pos = (size_x//2, size_y//2)

    # Create circles and start timer.
    big_circle = EmptyCircle(x_pos, y_pos, big_circle_r)
    small_circle = EmptyCircle(x_pos, y_pos, small_circle_r)
    timer_10s = Timer(timer_length)

    # Font parameters and text initialization.
    pygame.font.init()
    myfont = pygame.font.SysFont('elephant', 80)
    text_timer = Text('', 0, 0)

    # Start coordinates of MPU6050.
    cursor = Cursor(size_x)
    #t0 = time.time()
    #next_t = dt

    # Starting game.
    difficulty = 1
    bg_color = red
    run = True
    while run:
        pygame.time.delay(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        if big_circle.cursor_is_inside():
            if not small_circle.cursor_is_inside():
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
            if difficulty == 9:
                display_congrats(display)
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
        #display.blit(textsurface, (x_pos - 30, 75 ))
        text_timer.draw(display, x_pos - 30, 75)

        # Get position of the mouse cursor and draw a red circle on it.
        #pygame.draw.circle(display, black, pygame.mouse.get_pos(), cursor_r)
        cursor.draw(display)
        pygame.display.update()

    pygame.quit()