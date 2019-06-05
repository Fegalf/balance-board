# Running the Balance Board Game

1. Download the project from this repository.
2. Open a terminal and browse to the balance-board folder.
3. Make sure all dependencies are installed (see below).
3. In the terminal, run `python3 level_1.py` to start the level 1 of the Balance Board Game.
4. The game will create a file (mesures.csv), containing the measurements of MPU6050 data.
6. After the game session, sum-up graphics will be displayed. 

# Dependencies
To run the program from a python shell, the following dependencies are required (install in python 3 version using `pip3`; e.g. `pip3 install pygame`):

- pygame
- matplotlib
- numpy
- smbus2

# Connexions du RaspberryPi
- VCC du MPU6050 --> pin 1 (3.3V) du Raspberry Pi (RPi),
- GND du MPU6050 --> pin 6 (GND) du RPi,
- SDA du MPU6050 --> pin 3 (SDA) du RPi,
- SCL du MPU6050 --> pin 5 (SCL) du RPi. 

