import sqlite3
import os

class DbInterface:
	def __init__(self, db_path):
		self.conn = sqlite3.connect(db_path)
