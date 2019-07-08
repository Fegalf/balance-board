from smbus2 import SMBus
import math

class MPU6050:
    def __init__(self,):
        self.bus = SMBus(1)
        self.address = 0x68
        self.bus.write_byte_data(self.address, 0x6b, 0)
        self.bus.write_byte_data(self.address, 26, 3)

    def read_data(self,):
        raw_data = self.bus.read_i2c_block_data(self.address, 0x3B, 14)
        acc_x = (raw_data[0] << 8) + raw_data[1]

        if acc_x >= 0x8000:
            acc_x = -((65535 - acc_x) + 1)
        acc_x = acc_x / 16384.0
        acc_y = (raw_data[2] << 8) + raw_data[3]

        if acc_y >= 0x8000:
            acc_y = -((65535 - acc_y) + 1)
        acc_y = acc_y / 16384.0
        acc_z = (raw_data[4] << 8) + raw_data[5]

        if acc_z >= 0x8000:
            acc_z = -((65535 - acc_z) + 1)

        acc_z = acc_z / 16384.0
        z2 = acc_z * acc_z
        x_rot = math.degrees(math.atan2(acc_y, math.sqrt((acc_x * acc_x) + z2)))
        y_rot = -math.degrees(math.atan2(acc_x, math.sqrt((acc_y * acc_y) + z2)))
        gyro_x = (raw_data[8] << 8) + raw_data[9]

        if gyro_x >= 0x8000:
            gyro_x = -((65535 - gyro_x) + 1)

        gyro_x = gyro_x / 131.0
        gyro_y = (raw_data[10] << 8) + raw_data[11]

        if gyro_y >= 0x8000:
            gyro_y = -((65535 - gyro_y) + 1)
        gyro_y = gyro_y / 131.0

        return -x_rot, y_rot, acc_z, -gyro_x, gyro_y

