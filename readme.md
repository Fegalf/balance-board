# Running the Balance Board Game

1. Download the project from this repository.
2. Open a terminal and browse to the balance-board folder.
3. Make sure all dependencies are installed (see below).
3. In the terminal, run `python3 level_1.py` to start the level 1 of the Balance Board Game.
4. The game will create a file (mesures.csv), containing the measurements of MPU6050 data.
6. After the game session, sum-up graphics will be displayed. 

# Modify the game parameters 
In each level's code (e.g. `level_1.py`), you find a block of code containing all the ajustable paramters of the level. 
For the first level, it looks like

```
################### LEVEL PARAMETERS ###################

BIG_CIRCLE_RADIUS = 150 # in pixels.
TIME_BETWEEN_DIFFICULTY_CHANGES = 10  # in seconds.
GAIN_OF_MPU6050 = 10  # arbitrary value (test for other gain values).
N_DIFFICULTY_LEVELS = 9

########################################################
```
Here, you can, for exemple, adjust the radius of the outter circle (i.e. big circle) by changing the value of `BIG_CIRCLE_RADIUS`. 

# Dependencies
To run the program from a python shell, the following dependencies are required (install in python 3 version using `pip3`; e.g. `pip3 install pygame`):

- pygame
- matplotlib
- numpy
- smbus2

# Connections of MPU6050 to the RaspberryPi
- VCC of MPU6050 --> pin 1 (3.3V),
- GND of MPU6050 --> pin 6 (GND),
- SDA of MPU6050 --> pin 3 (SDA),
- SCL of MPU6050 --> pin 5 (SCL). 

