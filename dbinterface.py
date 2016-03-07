import sqlite3
import os

class DbInterface:
	def __init__(self, db_path):
		
		# open connection
		self.conn = sqlite3.connect(db_path)
		
		# create user table
		cur =  self.conn.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS users " +
								"(user_id INTEGER, " +
								"reputation INTEGER, " +
								"CONSTRAINT users_pk PRIMARY KEY (user_id))")
		
		# don't forget to commit!
		self.conn.commit()
								
	def close(self):
		self.conn.close()
		
	def adduser(self, userid, startingrep):
		cur = self.conn.cursor()
		
		cur.execute("INSERT INTO users (user_id, reputation) VALUES (?,?)", 
									(userid, startingrep))
		
		self.conn.commit()