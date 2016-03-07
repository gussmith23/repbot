import sqlite3

class DbInterface:
	def __init__(self):
		self.conn = sqlite3.connect("repbot.db")
