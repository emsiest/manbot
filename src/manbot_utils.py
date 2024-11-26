import json
import string
import random
from pathlib import Path

'''
Helper methods.
'''

this_dir = Path(__file__).parent
class ManbotUtils:
	all_categories = {}
	all_men = {}
	purple = 0x7800b4

	def __init__(self):
		with open(this_dir / 'resources/categories.json') as f:
			ManbotUtils.all_categories = json.load(f)

		with open(this_dir / 'resources/men.json') as f:
			ManbotUtils.all_men = json.load(f)

	@staticmethod
	# try extracting category name from message
	def get_category(message_content, keyword):
		category = message_content.rpartition(keyword)[2]
		if category in ManbotUtils.all_categories.keys():
			return category
		return None

	@staticmethod
	# try extracting man name from message
	def get_man(message_content, keyword):
		name = message_content.rpartition(keyword)[2]
		if name in ManbotUtils.all_men.keys():
			return name
		return None

	@staticmethod
	def update_file(fileName, content):
		with open(this_dir / fileName, 'w') as file:
			json.dump(content, file)

	@staticmethod
	def read_file(fileName):
		with open(this_dir / fileName,'r') as file:
			return file.readlines()

	@staticmethod
	def clean_message(message):
		message.content = message.content.translate(str.maketrans('', '', string.punctuation))
		return

	@staticmethod
	# check for misspelled man names and bonk user if typo detected
	def check_typo(message):
		# only check first two words in the message
		split_message = str.split(message.content)
		if len(split_message) > 1:
			message_start = split_message[0] + " " + split_message[1]
		else:
			message_start = split_message

		for m in ManbotUtils.all_men.keys():
			edit_distance = ManbotUtils.edit_dist(m, message_start)
			if 0 < edit_distance < 3:
				jail_txt = ManbotUtils.read_file("images/hornyJail.txt")
				return random.choice(jail_txt) + " too thirsty to spell, huh " + message.author.mention + "? :wink:"

	@staticmethod
	# calculate edit distance between strings
	def edit_dist(s1, s2):
		m, n = len(s1), len(s2)
		prev = list(range(n + 1))

		# Rest of the rows
		for i in range(1, m + 1):
			curr = [i]  # j = 0
			for j in range(1, n + 1):
				if s1[i - 1] == s2[j - 1]:
					curr.append(prev[j - 1])
				else:
					curr.append(1 + min(curr[-1], prev[j], prev[j - 1]))
			prev = curr
		return prev[n]
