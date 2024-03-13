import random

from PIL import Image, ImageChops


def convert_c_and_p_to_r(direction):
    if direction == 'C':
        return 'R'
    elif direction == 'P':
        return 'R' if random.random() < 0.5 else 'P'
    else:
        return direction


def convert_c_to_r(direction):
    return 'R' if direction == 'C' else direction


def get_random_asset_filename(asset_type, max_index):
    return f'./assets/{asset_type}_{random.randint(0, max_index)}.png'


def random_flipper(asset_to_flip):
    return asset_to_flip.transpose(Image.FLIP_LEFT_RIGHT) if random.random() < 0.5 else asset_to_flip


def get_rotated_asset(asset, rotation):
    return asset.rotate(rotation, expand=True) if rotation else asset


def get_asset_orientation(up, down, left, right, character):
    directions = [str(up), str(down), str(left), str(right)]
    character = str(character)
    return ''.join([character if direction == character else 'N' for direction in directions])


def surroundings(x, y, matrix):
    up = 'P' if y > 0 and matrix[y - 1][x] == 'P' else 'N'
    down = 'P' if y < len(matrix) - 1 and matrix[y + 1][x] == 'P' else 'N'
    left = 'P' if x > 0 and matrix[y][x - 1] == 'P' else 'N'
    right = 'P' if x < len(matrix[0]) - 1 and matrix[y][x + 1] == 'P' else 'N'

    return (up, down, left, right)


def are_images_equal(img1, img2):
    equal_size = img1.height == img2.height and img1.width == img2.width

    if img1.mode == img2.mode == "RGBA":
        img1_alphas = [pixel[3] for pixel in img1.getdata()]
        img2_alphas = [pixel[3] for pixel in img2.getdata()]
        equal_alphas = img1_alphas == img2_alphas
    else:
        equal_alphas = True

    equal_content = not ImageChops.difference(
        img1.convert("RGB"), img2.convert("RGB")
    ).getbbox()

    return equal_size and equal_alphas and equal_content