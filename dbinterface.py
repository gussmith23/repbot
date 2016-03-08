import sqlite3
import os
import time
import queue
import threading

class DbInterface:
	def __init__(self, db_path):
				
		self.q = queue.Queue()
		
		# setup&start thread that will handle db accesses
		t = threading.Thread(target = worker)
		t.start()
				
	def adduser(self, userid, username, startingrep):
		
		added = False
		
		returnlist = []
		
		query = ("INSERT INTO users (user_id, reputation, username, time_joined) VALUES (?,?,?,?)", 
							(userid, startingrep, username, int(time.time())),
							returnlist)
							
		self.q.put(query)
		
		# block until worker processes our query.
		while len(returnlist) == 0:
			pass
			
		if returnlist[0] == False:
			added = False
		else:
			added = True
			
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
		
	def worker(self):
	
		# open connection. this object should ONLY be touched
		# by this worker loop.
		# TODO: remove 'self.' so that it's local to this loop.
		self.conn = sqlite3.connect(db_path)
		
		# create user table
		cur =  self.conn.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS users " +
								"(user_id INTEGER, " +
								"reputation INTEGER, " +
								"username TEXT," +
								"time_joined INTEGER," +
								"CONSTRAINT users_pk PRIMARY KEY (user_id))")
		
		# don't forget to commit!
		self.conn.commit()
		
		while True:
			query = self.q.get()
			if query is None: continue
			
			# query structure will be a tuple with the following items:
			# first, a string query (required)
			# second, a tuple of fill-in arguments for the query (required, can be empty)
			# third, an empty list for getting return values. (required even if no returns given)
			# TODO i don't like this structure; second and third shouldn't be required
			
			cur = self.conn.cursor()
			
			error = False
			
			# executing with arguments
			if len(query) > 1:
				try:	
					cur.execute(query[0], query[1])
				except sqlite3.IntegrityError:
					error = True
				
			# executing without arguments
			else:
				try:	
					cur.execute(query[0])
				except sqlite3.IntegrityError:
					error = True				
					
			# handle error case and exit if error 
			if error:
				query[2].extend([False])
				self.q.task_done()
				continue
					
			# if there's no return, we signal with "None"
			all = cur.fetchall()
			if (len(all) == 0): 
				query[2].extend([None])
			else:	
				query[2].extend(all)
				
			# finally, commit.
			self.conn.commit()
			
			q.task_done()
				