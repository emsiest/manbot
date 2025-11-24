import unittest
from unittest.mock import MagicMock

from src.manbot_utils import ManbotUtils


class TestManbotUtils(unittest.TestCase):

	def setUp(self):
		ManbotUtils()

	def test_init(self):
		self.assertIsNotNone(ManbotUtils.all_categories)
		self.assertIsNotNone(ManbotUtils.all_men)

	def test_get_category_success(self):
		category = ManbotUtils.get_category("MANBOT DISABLE ANIME", " DISABLE ")
		self.assertEqual(category, "ANIME")

	def test_get_category_empty(self):
		category = ManbotUtils.get_category("MANBOT DISABLE", " DISABLE ")
		self.assertIsNone(category)

	def test_get_man_success(self):
		man = ManbotUtils.get_man("MANBOT DISABLE LAN WANGJI", " DISABLE ")
		self.assertEqual(man, "LAN WANGJI")

	def test_get_man_missing(self):
		man = ManbotUtils.get_man("MANBOT DISABLE WILL SMITH", " DISABLE ")
		self.assertIsNone(man)

	def test_edit_dist(self):
		self.assertEqual(ManbotUtils.edit_dist("hello", "hell"), 1)
		self.assertEqual(ManbotUtils.edit_dist("hello", "halo"), 2)
		self.assertEqual(ManbotUtils.edit_dist("hello", "mallow"), 3)

	def test_clean_message(self):
		mock_message = MagicMock(content="hello??")
		print(ManbotUtils.clean_message(mock_message))
		self.assertEqual(ManbotUtils.clean_message(mock_message).content, "hello")

	def test_check_typo(self):
		mock_message = MagicMock(content="ZANG ZEHAN")
		self.assertTrue(ManbotUtils.check_typo(mock_message).endswith(":wink:"))
		mock_message = MagicMock(content="ZHANG ZEHHNA")
		self.assertIsNone(ManbotUtils.check_typo(mock_message))
		mock_message = MagicMock(content="Xu Si")
		self.assertIsNone(ManbotUtils.check_typo(mock_message))

if __name__ == '__main__':
	unittest.main()
