import random

from task2.utils.utils import convert_c_to_r


def rotate_car(x, y, matrix, car_asset_image):
    up = convert_c_to_r(matrix[y - 1][x]) if y > 0 else 'N'
    down = convert_c_to_r(matrix[y + 1][x]) if y < len(matrix) - 1 else 'N'
    left = convert_c_to_r(matrix[y][x - 1] if x > 0 else 'N')
    right = convert_c_to_r(matrix[y][x + 1] if x < len(matrix[0]) - 1 else 'N')

    if up == 'R' and down == 'R' and left == 'R' and right == 'R':
        return car_asset_image.rotate(random.randint(0, 90))

    if right == 'R' or left == 'R':

        return car_asset_image.rotate(90, expand=True)
    else:
        return car_asset_image


