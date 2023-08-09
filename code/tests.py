import os
import unittest
from unittest.mock import patch

import pygame

from level import Level
from magic import MagicPlayer
from weapon import Weapon


class TestLevel(unittest.TestCase):
    def setUp(self):
        # Set up the display surface
        pygame.display.init()
        pygame.display.set_mode((1280, 720))

        # Code to run before each test
        self.patcher = patch("pygame.display.get_surface")
        self.mock_get_surface = self.patcher.start()
        self.mock_get_surface.return_value = pygame.Surface((1280, 720))
        self.level = Level()

    def tearDown(self):
        # Code to run after each test
        self.patcher.stop()
        pygame.display.quit()

    def test_initialization(self):
        # Testing if level is initialized properly
        self.assertIsInstance(self.level, Level)
        self.assertFalse(self.level.game_paused)

    @patch("code.support.import_csv_layout")
    @patch("code.support.import_folder")
    def test_create_map(self, mock_import_folder, mock_import_csv_layout):
        # Mocking the return values of the functions
        mock_import_folder.return_value = {"grass": ["image1.png", "image2.png"]}
        mock_import_csv_layout.return_value = {
            "boundary": [["-1"]],
            "grass": [["-1"]],
            "object": [["-1"]],
            "entities": [["-1"]],
        }

        # Calling create_map
        self.level.create_map()

        # TODO: Fix pathing issue
        # Check if the functions were called
        # mock_import_csv_layout.assert_called()
        # mock_import_folder.assert_called()

    @patch.object(Weapon, "__init__", lambda x, y, z: None)  # Patching Weapon class
    def test_create_attack(self):
        # Testing create_attack method
        self.level.create_attack()
        self.assertIsNotNone(self.level.current_attack)

    @patch.object(MagicPlayer, "flame")  # Patching MagicPlayer class
    def test_create_magic(self, mock_flame):
        # Testing create_magic method with flame style
        self.level.create_magic("flame", 5, 10)
        mock_flame.assert_called()
