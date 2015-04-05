#!/usr/bin/python

import re as regex
import datetime


class log:

	
	def __init__(self,email):
		title = email.subject
		date = "03-04-15" 
		time = "01:00:21"
		server = email.host
		port = email.port
		sender = email.sender
		to = email.reciever
		
	def write_log(self):
		date = "03-04-15" 
		time = "01:00:21"
		fname = date+"_"+time+".log"
		f = open(fname,"w+")
		log = "#Email Sent transaction log\nDate = "+date+"\n"+"Time = "+time+"\n"+"Server = "+self.server+"\n"+"Port = "+self.port+"\n"+"To = "+self.to+"\n"+"From = "+self.sender
		f.write(log)
		f.close()

def check_email(email):
	email_regex = regex.compile("^[_A-Za-z0-9-]+(\\.[_A-Za-z0-9-]+)*@[A-Za-z0-9-]+(\\.[A-Za-z0-9-]+)*(\\.[A-Za-z]{2,})$")
	if not email_regex.match(email):
		return False
	else:
		return True
