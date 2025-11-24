import discord
import unittest
from discord.ext import commands
from discord.ui.view import View
from unittest.mock import MagicMock

from general_commands import (get_help_embed, get_list_categories_embed, get_list_men_embed, get_stats_embed)
from man_commands import (get_random_embed, get_man)

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

    def test_list_categories(self):
        self.assertEqual(get_list_categories_embed(get_mock_context("MANBOT CATEGORIES")).title, "ALL CATEGORIES")
        self.assertEqual(get_list_categories_embed(get_mock_context("MANBOT CATEGORIES ANIME")).title, "ANIME SUBCATEGORIES")

    def test_list_men(self):
        self.assertEqual(get_list_men_embed(get_mock_context("MANBOT MEN ANIME")).title, "ANIME MEN")

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
