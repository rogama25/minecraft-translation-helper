import json

class Translations:
	def __init__(self):
		self.first_file_lines = None
		self.is_translation_line = None
		self.first_file_keys = None
		self.first_file_translations = None
		self.second_file_translations = None
		self.common_keys = None
		self.first_file_uri = None
		self.second_file_uri = None
	
	def load_first(self):
		self.first_file_translations = {}
		with open(self.first_file_uri, mode='r+', encoding="utf-8") as file:
			self.first_file_translations = json.load(file)
			for k in self.first_file_translations:
				if k.startswith("_"):
					self.first_file_translations.pop(k, None)
			self.first_file_translations.pop("_comment", None)

	def load_second(self):
		self.second_file_translations = {}
		with open(self.second_file_uri, mode='r+', encoding="utf-8") as file:
			self.second_file_translations = json.load(file)
			for k in self.second_file_translations:
				if k.startswith("_"):
					self.second_file_translations.pop(k, None)
			self.recalculate_common()

	def recalculate_common(self):
		self.common_keys = []
		for key in self.first_file_translations:
			if key in self.second_file_translations:
				self.common_keys.append(key)
	
	def save_second(self):
		line_number = 0
		with open(self.second_file_uri, "w+", encoding="utf-8") as file:
			json.dump(self.second_file_translations, file, ensure_ascii=False, indent="\t")
