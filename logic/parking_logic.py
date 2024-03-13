from task2.utils.utils import get_asset_orientation, get_rotated_asset, surroundings


def place_all_parking_marks(matrix, all_assets_images, map_image):
    for y, line in enumerate(matrix):
        for x, char in enumerate(line):
            if char == 'P' or is_mostly_parking(x, y, matrix):
                position = (x * all_assets_images['road'].size[0], y * all_assets_images['road'].size[1])
                map_image.paste(all_assets_images['parking_mark'], position, all_assets_images['parking_mark'])



def is_mostly_parking(x, y, matrix):
    up, down, left, right = surroundings(x, y, matrix)
    key = ''.join([direction for direction in (up, down, left, right)])
    if key.count('P') > 2:
        return True
    else:
        return False



def get_parking_asset(x, y, matrix, all_assets_images):
    surroundings_local = lambda: (
        'P' if y > 0 and matrix[y - 1][x] == 'P' else 'N',
        'P' if y < len(matrix) - 1 and matrix[y + 1][x] == 'P' else 'N',
        'P' if x > 0 and matrix[y][x - 1] == 'P' else 'N',
        'P' if x < len(matrix[0]) - 1 and matrix[y][x + 1] == 'P' else 'N')

    up, down, left, right = surroundings_local()

    if y > 0 and is_mostly_parking(x, y - 1, matrix) and matrix[y - 1][x] == 'C':
        up = 'P'
    if y < len(matrix) - 1 and is_mostly_parking(x, y + 1, matrix) and matrix[y + 1][x] == 'C':
        down = 'P'
    if x > 0 and is_mostly_parking(x - 1, y, matrix) and matrix[y][x - 1] == 'C':
        left = 'P'
    if x < len(matrix[0]) - 1 and is_mostly_parking(x + 1, y, matrix) and matrix[y][x + 1] == 'C':
        right = 'P'

    direction_to_asset = {
        'PNPN': ('parking_corner', None), 'PNNP': ('parking_corner', 270),
        'NPNP': ('parking_corner', 180), 'NPPN': ('parking_corner', 90),
        'PNPP': ('parking_side', 270), 'NPPP': ('parking_side', 90),
        'PPPN': ('parking_side', None), 'PPNP': ('parking_side', 180),
        'NNPP': ('parking_double', 90), 'PPNN': ('parking_double', None),
        'PNNN': ('parking_bulge', None), 'NPNN': ('parking_bulge', 180),
        'NNPN': ('parking_bulge', 90), 'NNNP': ('parking_bulge', 270),
        'NNNN': ('parking_single', None)
    }

    key = get_asset_orientation(up, down, left, right, 'P')
    asset_name, rotation = direction_to_asset.get(key, ('parking_center', None))
    return get_rotated_asset(all_assets_images[asset_name], rotation)

