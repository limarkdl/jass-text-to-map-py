from PIL import Image

from task2.utils.utils import get_random_asset_filename, convert_c_to_r


def get_sidewalk_assets(x, y, matrix, all_assets_images):
    up = convert_c_to_r(matrix[y - 1][x] if y > 0 else 'N')
    down = convert_c_to_r(matrix[y + 1][x] if y < len(matrix) - 1 else 'N')
    left = convert_c_to_r(matrix[y][x - 1] if x > 0 else 'N')
    right = convert_c_to_r(matrix[y][x + 1] if x < len(matrix[0]) - 1 else 'N')
    orientation = ''.join(tile if tile in ['R', 'S'] else 'N' for tile in [up, down, left, right])

    asset, rotation, transpose_direction = {
        'SSNR': ('sidewalk_side', None, None), 'RNNS': ('sidewalk_end', 180, 'Flip_H'),
        'RNSN': ('sidewalk_end', 180, None),
        'NRSN': ('sidewalk_end', None, 'Flip_H'),
        'NRNS': ('sidewalk_end', None, None), 'RNSS': ('sidewalk_flip', 0, None),
        'RNRS': ('sidewalk_corner_end', 180, None),
        'RNSR': ('sidewalk_corner_end', 180, 'Flip_H'),
        'NRSR': ('sidewalk_corner_end', 0, None),
        'NRRS': ('sidewalk_corner_end', 0, 'Flip_H'),
        'SNRN': ('sidewalk_end', 90, 'Flip_H'),
        'SRSR': ('sidewalk_corner', 0, None),
        'SRSS': ('sidewalk_trio_fork', 0, None),
        'SSRN': ('sidewalk_side', 0, 'Flip_H'),
        'SSRR': ('sidewalk_universal', 90, None),
        'SRNS': ('sidewalk_corner', 0, 'Flip_H'),
        'RSNR': ('sidewalk_corner_end', 90, None),
        'NSSR': ('sidewalk_corner', 90, None), 'NSNS': ('sidewalk_corner_small', 0, None),
        'SSNS': ('sidewalk_corner', 180, None),
        'SRNR': ('sidewalk_corner_end', 270, 'Flip_H'),
        'SNRS': ('sidewalk_corner', 0, 'Flip_H'),
        'SNNS': ('sidewalk_corner_small', 180, 'Flip_H'),
        'RSRS': ('sidewalk_corner', 180, None), 'NSRS': ('sidewalk_corner', 180, None),
        'SRSN': ('sidewalk_corner', 0, None), 'NSSN': ('sidewalk_corner', 90, None),
        'RSNN': ('sidewalk_end', 270, None),
        'NNSR': ('sidewalk_end', 0, 'Flip_H'), 'NNRS': ('sidewalk_end', 0, None),
        'SNNN': ('sidewalk_end', 90, None), 'SRNN': ('sidewalk_end', 90, None),
        'SNSR': ('sidewalk_corner', 0, None),
        'SRRS': ('sidewalk_corner', 0, 'Flip_H'),
        'RNNR': ('sidewalk_corner_independent', 90, None),
        'SSNN': ('sidewalk_center', 0, None),
        'NNNS': ('S', 0, None), 'NNSN': ('sidewalk_universal', 0, None),
        'RSSS': ('sidewalk_trio_fork', 180, None), 'NSSS': ('sidewalk_universal', 0, None),
        'RSSN': ('sidewalk_universal', 0, None),
        'SSSN': ('sidewalk_universal', 90, None), 'RRSS': ('sidewalk_universal', 0, None),
        'SSSS': ('sidewalk_universal', 90, None), 'RRSR': ('sidewalk_trio', 0, None),
        'RRRS': ('sidewalk_trio', 180, None), 'RRNS': ('sidewalk_trio', 180, None),
        'RSNS': ('sidewalk_trio', 0, 'Flip_H'), 'RSSR': ('sidewalk_corner', 90, None),
        'SNSN': ('sidewalk_corner', 0, None),
        'NSNR': ('sidewalk_end', 270, 'Flip_H'),
        'NRRR': ('sidewalk_trio', 270, None),
        'SRRR': ('sidewalk_trio', 270, None),
        'RSRN': ('sidewalk_side', 0, 'Flip_H'),
        'SRRN': ('sidewalk_corner_end', 270, None),
        'SNNR': ('sidewalk_side', 0, None)
    }.get(orientation, ('S', None, None))
    image = Image.open(get_random_asset_filename('sidewalk', 1)) if asset == 'S' else all_assets_images[asset]
    image = image.rotate(rotation, expand=True) if rotation else image
    return image.transpose(Image.FLIP_LEFT_RIGHT) if transpose_direction == 'Flip_H' else image

