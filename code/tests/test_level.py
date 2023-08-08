import unittest
from unittest.mock import patch

from code.level import Level


class TestLevel(unittest.TestCase):
    def setUp(self):
        # Code to run before each test
        self.level = Level()

    def tearDown(self):
        # Code to run after each test
        pass

    def test_initialization(self):
        # Testing if level is initialized properly
        self.assertIsInstance(self.level, Level)
        self.assertFalse(self.level.game_paused)

    @patch("code.level.import_csv_layout")
    @patch("code.level.import_folder")
    def test_create_map(self, mock_import_folder, mock_import_csv_layout):
        # Mocking the return values of the functions
        mock_import_folder.return_value = {}
        mock_import_csv_layout.return_value = {
            "boundary": [["-1"]],
            "grass": [["-1"]],
            "object": [["-1"]],
            "entities": [["-1"]],
        }

        # Calling create_map
        self.level.create_map()

        # Check if the functions were called
        mock_import_csv_layout.assert_called()
        mock_import_folder.assert_called()

    @patch("code.level.Weapon")
    def test_create_attack(self, mock_weapon):
        # Testing create_attack method
        self.level.create_attack()
        mock_weapon.assert_called()

    @patch("code.level.MagicPlayer")
    def test_create_magic(self, mock_magic_player):
        # Testing create_magic method with flame style
        self.level.create_magic("flame", 5, 10)
        self.level.magic_player.flame.assert_called()
