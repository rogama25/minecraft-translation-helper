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
	
	def load_first(self, uri: str):
		self.first_file_lines = []
		self.is_translation_line = []
		self.first_file_keys = []
		self.first_file_translations = {}
		self.first_file_uri = uri
		with open(self.first_file_uri, mode='r+', encoding="utf-8") as file:
			for l in file:
				if ("=" not in l) or l.startswith("#"):
					self.first_file_lines.append(l)
					self.is_translation_line.append(False)
				else:
					key, value = l.split("=", 1)
					self.first_file_lines.append(key)
					self.is_translation_line.append(True)
					self.first_file_keys.append(key)
					if value.endswith("\n"):
						value = value[:-1]
					self.first_file_translations[key] = value

	def load_second(self, uri: str):
		self.second_file_translations = {}
		self.second_file_uri = uri
		with open(self.second_file_uri, mode='r+', encoding="utf-8") as file:
			for l in file:
				if ("=" in l) and not l.startswith("#"):
					key, value = l.split("=", 1)
					if value.endswith("\n"):
						value = value[:-1]
					self.second_file_translations[key] = value
					self.recalculate_common()

	def recalculate_common(self):
		self.common_keys = []
		for key in self.first_file_keys:
			if key in self.second_file_translations:
				self.common_keys.append(key)
	
	def save_second(self):
		line_number = 0
		with open(self.second_file_uri, "w+", encoding="utf-8") as file:
			for line in self.first_file_lines:
				if self.is_translation_line[line_number]:
					if line in self.second_file_translations:
						file.write(line + "=" + self.second_file_translations[line] + "\n")
				else:
					file.write(line)
				line_number += 1
