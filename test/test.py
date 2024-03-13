import os
import sys
import unittest
from unittest.mock import patch

from PIL import Image

sys.path.append(os.path.abspath(".."))

from task2.logic.parking_logic import get_parking_asset

from task2.utils.utils import get_asset_orientation, get_random_asset_filename, convert_c_and_p_to_r, convert_c_to_r, \
    random_flipper, get_rotated_asset, surroundings, are_images_equal


class TestGetAssetOrientation(unittest.TestCase):

    def test_all_match(self):
        self.assertEqual(get_asset_orientation('R', 'R', 'R', 'R', 'R'), 'RRRR')

    def test_no_match(self):
        self.assertEqual(get_asset_orientation('U', 'D', 'L', 'R', 'N'), 'NNNN')

    def test_mixed(self):
        self.assertEqual(get_asset_orientation('N', 'N', 'R', 'L', 'N'), 'NNNN')
        self.assertEqual(get_asset_orientation('R', 'N', 'N', 'R', 'R'), 'RNNR')

    def test_different_characters(self):
        self.assertEqual(get_asset_orientation('A', 'B', 'C', 'D', 'A'), 'ANNN')
        self.assertEqual(get_asset_orientation('1', '2', '2', '1', '1'), '1NN1')

    def test_numeric_values(self):
        self.assertEqual(get_asset_orientation(1, 2, 3, 4, 1), '1NNN')
        self.assertEqual(get_asset_orientation(5, 5, 6, 5, 5), '55N5')


class TestGetRandomAssetFilename(unittest.TestCase):

    def test_extension(self):
        self.assertTrue(get_random_asset_filename('sidewalk', 1).endswith('.png'))
        self.assertTrue(get_random_asset_filename('road', 1).endswith('.png'))
        self.assertTrue(get_random_asset_filename('parking', 1).endswith('.png'))

    def test_path(self):
        self.assertTrue(get_random_asset_filename('sidewalk', 1).startswith('./assets/sidewalk_'))
        self.assertTrue(get_random_asset_filename('road', 1).startswith('./assets/road_'))
        self.assertTrue(get_random_asset_filename('parking', 1).startswith('./assets/parking_'))

    @patch('random.randint', return_value=0)
    def test_index(self, mock_randint):
        self.assertTrue(get_random_asset_filename('sidewalk', 1).endswith('_0.png'))
        self.assertTrue(get_random_asset_filename('car', 1).endswith('_0.png'))
        self.assertTrue(get_random_asset_filename('parking', 1).endswith('_0.png'))


class ConvertCAndPToR(unittest.TestCase):

    def test_c(self):
        self.assertEqual(convert_c_and_p_to_r('C'), 'R')

    def test_p(self):
        self.assertIn(convert_c_and_p_to_r('P'), ['R', 'P'])

    def test_n(self):
        self.assertEqual(convert_c_and_p_to_r('N'), 'N')

    def test_not_c_not_p(self):
        self.assertEqual(convert_c_and_p_to_r('A'), 'A')


class TestConvertCtoR(unittest.TestCase):

    def test_c(self):
        self.assertEqual(convert_c_to_r('C'), 'R')

    def test_p(self):
        self.assertEqual(convert_c_to_r('P'), 'P')

    def test_n(self):
        self.assertEqual(convert_c_to_r('N'), 'N')

    def test_not_c(self):
        self.assertEqual(convert_c_to_r('A'), 'A')


class TestRandomFlipper(unittest.TestCase):

    @patch('random.random', return_value=0.5)
    def test_flip_not_happening(self, mock_random):
        asset_to_flip = Image.new('RGB', (100, 100), color='red')
        flipped_asset = random_flipper(asset_to_flip)
        self.assertEqual(asset_to_flip, flipped_asset)

    def test_flip_type_safe(self):
        asset_to_flip = Image.new('RGB', (100, 100), color='red')
        flipped_asset = random_flipper(asset_to_flip)
        self.assertEqual(type(asset_to_flip), type(flipped_asset))


class TestGetRotatedAsset(unittest.TestCase):

    def test_no_rotation(self):
        asset = Image.new('RGB', (100, 100), color='red')
        rotated_asset = get_rotated_asset(asset, 0)
        self.assertTrue(asset, rotated_asset)

    def test_rotation(self):
        asset = Image.new('RGB', (100, 200), color='red')
        rotated_asset = get_rotated_asset(asset, 90)

        self.assertEqual(rotated_asset.size, (200, 100))

    def test_rotation_type_safe(self):
        asset = Image.new('RGB', (100, 100), color='red')
        rotated_asset = get_rotated_asset(asset, 90)
        self.assertEqual(type(asset), type(rotated_asset))


class TestSurroundings(unittest.TestCase):

    def test_surrounded_by_parking(self):
        matrix = [
            ['P', 'P', 'P'],
            ['P', 'C', 'P'],
            ['P', 'P', 'P']
        ]
        self.assertEqual(surroundings(1, 1, matrix), ('P', 'P', 'P', 'P'))

    def test_no_parking_around(self):
        matrix = [
            ['N', 'N', 'N'],
            ['N', 'C', 'N'],
            ['N', 'N', 'N']
        ]
        self.assertEqual(surroundings(1, 1, matrix), ('N', 'N', 'N', 'N'))

    def test_parking_on_one_side(self):
        matrix = [
            ['N', 'N', 'N'],
            ['P', 'C', 'N'],
            ['N', 'N', 'N']
        ]
        self.assertEqual(surroundings(1, 1, matrix), ('N', 'N', 'P', 'N'))

    def test_corner_case_top_left(self):
        matrix = [
            ['C', 'N'],
            ['P', 'N']
        ]
        self.assertEqual(surroundings(0, 0, matrix), ('N', 'P', 'N', 'N'))

    def test_corner_case_bottom_right(self):
        matrix = [
            ['N', 'P'],
            ['N', 'C']
        ]
        self.assertEqual(surroundings(1, 1, matrix), ('P', 'N', 'N', 'N'))

    def test_edge_case_top_row(self):
        matrix = [
            ['N', 'C', 'P'],
            ['N', 'N', 'N'],
        ]
        self.assertEqual(surroundings(1, 0, matrix), ('N', 'N', 'N', 'P'))


class TestGetParkingAsset(unittest.TestCase):

    @patch('task2.logic.parking_logic.is_mostly_parking', return_value=True)
    @patch('task2.utils.utils.get_rotated_asset')
    def test_parking_corner(self, mock_get_rotated_asset, mock_is_mostly_parking):
        matrix = [
            ['C', 'P', 'N'],
            ['P', 'P', 'N'],
            ['N', 'N', 'N']
        ]
        all_assets_images = {'parking_corner': 'fake_parking_corner_asset'}
        get_parking_asset(1, 1, matrix, all_assets_images)
        print()
        self.assertEqual(get_parking_asset(1, 1, matrix, all_assets_images), 'fake_parking_corner_asset')

    @patch('task2.logic.parking_logic.is_mostly_parking', return_value=True)
    @patch('task2.utils.utils.get_rotated_asset')
    def test_parking_side(self, mock_get_rotated_asset, mock_is_mostly_parking):
        matrix = [
            ['P', 'P', 'N'],
            ['C', 'P', 'N'],
            ['P', 'P', 'N']
        ]
        all_assets_images = {'parking_side': 'fake_parking_side_asset'}
        get_parking_asset(1, 1, matrix, all_assets_images)
        self.assertEqual(get_parking_asset(1, 1, matrix, all_assets_images), 'fake_parking_side_asset')

    @patch('task2.logic.parking_logic.is_mostly_parking', return_value=True)
    @patch('task2.utils.utils.get_rotated_asset')
    def test_parking_center(self, mock_get_rotated_asset, mock_is_mostly_parking):
        matrix = [
            ['P', 'P', 'N'],
            ['C', 'P', 'P'],
            ['P', 'P', 'N']
        ]
        all_assets_images = {'parking_center': 'fake_parking_center_asset'}
        get_parking_asset(1, 1, matrix, all_assets_images)
        self.assertEqual(get_parking_asset(1, 1, matrix, all_assets_images), 'fake_parking_center_asset')

    @patch('task2.logic.parking_logic.is_mostly_parking', return_value=True)
    @patch('task2.utils.utils.get_rotated_asset')
    def test_parking_corner_2(self, mock_get_rotated_asset, mock_is_mostly_parking):
        mock_image = Image.new('RGB', (100, 100))
        mock_get_rotated_asset.return_value = mock_image

        matrix = [
            ['N', 'P', 'N'],
            ['C', 'P', 'P'],
            ['P', 'N', 'N']
        ]
        all_assets_images = {'parking_side': mock_image}
        result = get_parking_asset(1, 1, matrix, all_assets_images)

        self.assertTrue(are_images_equal(result, mock_image))


if __name__ == '__main__':
    unittest.main()