import discord
import unittest
from discord.ext import commands
from discord.ui.view import View
from unittest.mock import MagicMock, patch

from general_commands import (get_help_embed, get_list_categories_embed, get_list_men_embed, get_stats_embed)
from man_commands import (get_random_embed, get_man)
from user_commands import (get_disable_embed, get_enable_embed, get_my_categories_embed, get_my_men_embed, get_reset_embed)
from manbot_utils import ManbotUtils

'''
Stateless unit tests.
'''

def get_mock_context(content):
    mock_message = MagicMock(content=content)
    mock_context = MagicMock(message=mock_message)
    return mock_context

class TestManbotCommands(unittest.TestCase):

    def setUp(self):
        self.bot = commands.Bot(command_prefix="MANBOT ", intents=discord.Intents.all())
        self.view = MagicMock(View)

    def test_help(self):
        self.assertEqual(get_help_embed(get_mock_context("MANBOT HELP")).title, "HELP MENU")

    @patch.object(ManbotUtils, 'update_file')
    def test_disable(self, mock_update_file):
        mock_update_file.return_value = None
        self.assertEqual(get_disable_embed(get_mock_context("MANBOT DISABLE ANIME")).title, "WOOHOO")
        self.assertEqual(get_disable_embed(get_mock_context("MANBOT DISABLE LAN WANGJI")).title, "WOOHOO")
        self.assertEqual(get_disable_embed(get_mock_context("MANBOT DISABLE")).title, "HEY")

    @patch.object(ManbotUtils, 'update_file')
    def test_enable(self, mock_update_file):
        mock_update_file.return_value = None
        self.assertEqual(get_enable_embed(get_mock_context("MANBOT ENABLE ANIME")).title, "HOLD UP")
        self.assertEqual(get_enable_embed(get_mock_context("MANBOT ENABLE LAN WANGJI")).title, "HOLD UP")
        self.assertEqual(get_enable_embed(get_mock_context("MANBOT ENABLE")).title, "HEY")

    @patch.object(ManbotUtils, 'update_file')
    def test_reset(self, mock_update_file):
        mock_update_file.return_value = None
        self.assertEqual(get_reset_embed(get_mock_context("MANBOT RESET ME")).title, "WOOHOO")

    def test_list_categories(self):
        self.assertEqual(get_list_categories_embed(get_mock_context("MANBOT CATEGORIES")).title, "ALL CATEGORIES")
        self.assertEqual(get_list_categories_embed(get_mock_context("MANBOT CATEGORIES ANIME")).title, "ANIME SUBCATEGORIES")

    def test_list_men(self):
        self.assertEqual(get_list_men_embed(get_mock_context("MANBOT MEN ANIME")).title, "ANIME MEN")
        self.assertEqual(get_enable_embed(get_mock_context("MANBOT MEN")).title, "HEY")

    def test_my_categories(self):
        self.assertEqual(get_my_categories_embed(get_mock_context("MANBOT MY CATEGORIES")).title, "MANBOT MY CATEGORIES")

    def test_my_men(self):
        self.assertEqual(get_my_men_embed(get_mock_context("MANBOT MY MEN")).title, "MANBOT MY MEN")

    def test_random(self):
        self.assertEqual(get_random_embed(get_mock_context("MANBOT RANDOM KPOP")).title, "RANDOM")
        self.assertEqual(get_random_embed(get_mock_context("MANBOT RANDOM")).title, "RANDOM")

    def test_stats(self):
        self.assertEqual(get_stats_embed(get_mock_context("MANBOT STATS")).title, "MANBOT STATS")
        self.assertTrue(get_stats_embed(get_mock_context("MANBOT STATS ANIME")).title.startswith("MANBOT STATS"))
        self.assertEqual(get_stats_embed(get_mock_context("MANBOT STATS HU GE")).title, "MANBOT STATS")

    def test_get_man(self):
        self.assertIsNotNone(get_man(MagicMock(content="ZHANG ZHEHAN")))
        self.assertIsNotNone(get_man(MagicMock(content="I love ZHANG ZHEHAN!")))
