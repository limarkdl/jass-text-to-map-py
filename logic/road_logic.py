from PIL import Image


from task2.utils.utils import convert_c_and_p_to_r, get_random_asset_filename, get_rotated_asset


def optimize_get_road_asset(x, y, matrix, all_assets_images):
    up = convert_c_and_p_to_r(matrix[y - 1][x]) if y > 0 else 'N'
    down = convert_c_and_p_to_r(matrix[y + 1][x]) if y < len(matrix) - 1 else 'N'
    left = convert_c_and_p_to_r(matrix[y][x - 1]) if x > 0 else 'N'
    right = convert_c_and_p_to_r(matrix[y][x + 1]) if x < len(matrix[0]) - 1 else 'N'

    key = ''.join([direction if direction == 'R' else 'N' for direction in (up, down, left, right)])

    direction_to_asset = {
        'RRRR': ('road_cross', None), 'RRNN': ('road', 90), 'NNRR': ('road', None), 'NRNR': ('road_turn', 90),
        'NRRN': ('road_turn', None), 'RNRN': ('road_turn', 270), 'RNNR': ('road_turn', 180), 'RNNN': ('road_end', 90),
        'NRNN': ('road_end', 270), 'NNRN': ('road_end', 180), 'NNNR': ('road_end', None), 'RRRN': ('road_trio', None),
        'NRRR': ('road_trio', 90), 'RNRR': ('road_trio', 270), 'RRNR': ('road_trio', 180),
    }

    asset_name, rotation = direction_to_asset.get(key, ('road', None))
    if (asset_name == 'road_trio'):
        return get_rotated_asset(Image.open(get_random_asset_filename('road_trio', 1)), rotation)

    return get_rotated_asset(all_assets_images[asset_name], rotation)
