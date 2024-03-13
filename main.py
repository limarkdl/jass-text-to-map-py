import sys
import os
from PIL import Image

sys.path.append(os.path.abspath(".."))


from task2.assets_paths import all_asset_paths
from task2.logic.car_logic import rotate_car
from task2.logic.parking_logic import get_parking_asset, is_mostly_parking, place_all_parking_marks
from task2.logic.road_logic import optimize_get_road_asset
from task2.logic.sidewalk_logic_optimization import get_sidewalk_assets
from task2.utils.utils import get_random_asset_filename, random_flipper


# data_file_path = './data.txt'
output_file_path = './output.png'
optimized_input_file_path = 'auto_enhanced_input.txt'


def main():
    greetings()

    all_assets_images = {key: Image.open(path) for key, path in all_asset_paths.items()}

    print("Enter your map data (end input with an empty line):")
    matrix = []
    while True:
        line = input('> ')
        if line == "":
            break
        matrix.append(line)

    cleaned_matrix = [s.replace(' ', '_') for s in matrix]
    max_length_row = max(len(s) for s in matrix)
    matrix = [s.ljust(max_length_row, 'G') for s in cleaned_matrix]
    print('\nOptimized:')
    print_matrix_with_borders(matrix)

    with open(optimized_input_file_path, 'w') as file:
        for row in (matrix):
            file.write(row + '\n')

    map_image = initialize_result_image(matrix, all_assets_images)

    place_tiles(matrix, all_assets_images, map_image),
    place_all_parking_marks(matrix, all_assets_images, map_image)

    map_image.save(output_file_path)
    map_image.show(output_file_path)

    print(
        '\n\n\nDone!\nYour result is stored in ./output.png\nYour normalized input is stored in '
        './auto_enhanced_input.txt \n\nWait, image is being opened...\n')


def initialize_result_image(matrix, all_assets_images):
    map_width, map_height = len(matrix[0]) * all_assets_images['road'].size[0], len(matrix) * \
                            all_assets_images['road'].size[1]
    return Image.new('RGB', (map_width, map_height))


def greetings():
    print('***********************************')
    print('*                                 *')
    print('*  JASS 2024 ASSIGNMENT - TASK 2  *')
    print('*                                 *')
    print('***********************************')
    print('\nThis program will generate a map based on the data file')
    print('\nR = Road | C = Car | P = Parking | S = Sidewalk | G = Grass | B = Building | T = Traffic Light')
    input('\nPress [Enter] to start...\n')


def print_matrix_with_borders(matrix):
    max_length_row = max(len(row) for row in matrix)
    horizontal_border = '+' + '-' * (max_length_row + 2) + '+'

    print(horizontal_border)

    for row in matrix:
        print('| ' + row.ljust(max_length_row) + ' |')

    print(horizontal_border)


def place_tiles(matrix, all_assets_images, map_image):
    global asset_image
    for y, line in enumerate(matrix):
        for x, char in enumerate(line):
            if char == 'R':
                asset_image = optimize_get_road_asset(x, y, matrix, all_assets_images)
            elif char == 'P':
                asset_image = get_parking_asset(x, y, matrix, all_assets_images)
                mark_asset = all_assets_images['parking_mark']
                map_image.paste(mark_asset,
                                (x * all_assets_images['road'].size[0], y * all_assets_images['road'].size[1]))
            elif char == 'S':
                asset_image = get_sidewalk_assets(x, y, matrix, all_assets_images)
            elif char == 'G':
                asset_image = random_flipper(Image.open(get_random_asset_filename('grass', 1)))
            elif char == 'B':
                asset_image = random_flipper(Image.open(get_random_asset_filename('building', 2)))
            elif char == 'T':
                asset_image = all_assets_images['traffic_light']
            elif char in ['C']:
                asset_image = Image.open(get_random_asset_filename('car', 2))
                if char == 'C':
                    if is_mostly_parking(x, y, matrix):
                        extra_asset = get_parking_asset(x, y, matrix, all_assets_images)
                    else:
                        extra_asset = optimize_get_road_asset(x, y, matrix, all_assets_images)
                    asset_image = random_flipper(rotate_car(x, y, matrix, asset_image))
                    map_image.paste(extra_asset,
                                    (x * all_assets_images['road'].size[0], y * all_assets_images['road'].size[1]))
            else:
                asset_image = all_assets_images['404']
            if asset_image:
                map_image.paste(asset_image,
                                (x * all_assets_images['road'].size[0], y * all_assets_images['road'].size[1]),
                                asset_image if asset_image.mode == 'RGBA' else None)


if __name__ == "__main__":
    main()
