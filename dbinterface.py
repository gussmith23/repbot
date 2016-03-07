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
		
		added = False
		
		try:
			cur.execute("INSERT INTO users (user_id, reputation) VALUES (?,?)", 
										(userid, startingrep))
			self.conn.commit()
			added = True
		except sqlite3.IntegrityError:
			added = False
			
		return added	
		
		
	def getrep(self, userid):
		cur = self.conn.cursor()
		
		# note the use of the comma to make it a one-element list
		cur.execute("SELECT reputation FROM users WHERE user_id = ?", 
									(userid,))
									
		return cur.fetchone()[0]
		
	def setrep(self, userid, newrep):
		cur = self.conn.cursor()
		
		cur.execute("UPDATE users SET reputation = ? WHERE user_id = ?",
									(newrep,userid))
									
		self.conn.commit()
		
	def incrementrep(self, userid, amount):
		cur = self.conn.cursor()
		
		self.setrep(userid, self.getrep(userid) + amount)
		
									