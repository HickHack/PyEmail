# This file generates a text file with settings
# Password will need to somehow be encrypted if stored in settings file
# Code written by Graham Murray 2015 www.graham-murray.com

#!/usr/bin/python
import re as regex
import socket
import time
import os
import smtplib


#Error messages
host_unreach = "** Host is unreachable or doesn't exist**"
port_error = "** Port number must be a valid integer eg(0-9) **"
port_range_error = "** Port number range must be between 1 and 65535 **"

class settingsDetails:
	
	def __init__(self,host,port,sender,username):
		self.host = host
		self.port = port
		self.sender = sender
		self.username = username

	def display_settings(self):
		print "\n\t\t\tSMTP Summary\n\tServer: "+self.host+"\tPort: "+str(self.port)+"\n\tSender: "+self.sender+"\tUsername: "+self.username
	

	
def set_settings():
	
	host = raw_input("SMTP server address @> ")
	if host == "":
		print "** Please define a host address **"
		set_settings()

	#Test if a connect can be made to host on specified port
	try:
		socket.gethostbyname(host.strip())
	except:
		print host_unreach
		set_settings()

	port = raw_input("SMTP port number @> ")

	try:
		port = int(port)
	except ValueError:
		print port_error

	if port <1 or port >65535: print port_range_error; set_settings()


	#Test if a connect can be made to host on specified port
	time.sleep(4)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(4)
	port_open = sock.connect_ex((host,port))
	sock.close()

	if port_open != 0:
		print "** "+host+" unreachable on port "+str(port)+" **"
		set_settings()
	else:
		print "Connection Successful"
	
	sender = raw_input("Please enter your email address (Sender) @> ")
	email_regex = regex.compile("^[_A-Za-z0-9-]+(\\.[_A-Za-z0-9-]+)*@[A-Za-z0-9-]+(\\.[A-Za-z0-9-]+)*(\\.[A-Za-z]{2,})$")
	if not email_regex.match(sender):
		print "** Incorrect email format 'someone@domain.com' **";
		sender = raw_input("Please enter your email address (Sender) @> ")
	

	details = [host,port,sender]
	return details
	
	
def verify_account(host,port,email):
	
	arr = email.split('@')
	username = arr[0]
	result = raw_input("Is your username '"+username+"'? (yes/no) @> ")
	if result == 'yes':
		os.system("stty -echo")
		PASSWORD = raw_input("Account Password: ")
		os.system("stty echo")
		USERNAME = arr[0]
	elif result == 'no':
		USERNAME = raw_input("Account Username: ")
		os.system("stty -echo")
		PASSWORD = raw_input("Account Password: ")
		os.system("stty echo")
	else:
		print "** Answer should be 'yes' or 'no'"
		exit()
	
	try:#Test if login details work
		conn = smtplib.SMTP(host, port)
		conn.starttls()
		if not conn.login(USERNAME, PASSWORD):
			print "** Login Failure **"
		else:
			print "Login Successful"
			detailobj = settingsDetails(host,port,email,USERNAME)
			return detailobj
	except smtplib.SMTPException:
		print "** SMTP auth error, please try again **"
		
	
	
def set_settings_file(detailsobj):
	#add error control here
	f= open("settings.txt","w+")
	new_settings = "Server Address = "+ str(detailsobj.host) +"\n"+ "SMPT Port = "+str(detailsobj.port)+"\n"+ "Sender = "+str(detailsobj.sender)	+"\n"+ "Username = "+str(detailsobj.username)
	f.write(new_settings)
	f.close()
	
	#check and add filesize to the file to check if modified since last write in append mode
	f= open("settings.txt","a+")
	fsize = os.stat("settings.txt").st_size
	f.write("\nFilesize = "+str(fsize))
	f.close()
	
	print "** Settings file successfully generated **"
	settingsDetails.display_settings(detailsobj)
	f.close()
	return '1'
	
def load_settings():
	f = open("settings.txt","r")
	result = f.readlines()
	f.close()
	if result == "":
		os.remove("settings.txt")
		check_settings()
	else:
		h = result[0].split("= ")
		host = str(h[1]).strip("\n")

		p = result[1].split("= ")
		port = str(p[1]).strip("\n")

		s = result[2].split("= ")
		sender = str(s[1]).strip("\n")

		u = result[3].split("= ")
		username = str(u[1]).strip("\n")
	
	print "\t\t\tSMTP Summary\n\tServer: "+host+"\tPort: "+port+"\n\tSender: "+sender+"\tUsername: "+username
	package = [host,port,sender,username]
	return package

def check_settings():
	if os.path.isfile("settings.txt"):
		f = open("settings.txt","r")
		fstream = f.readlines()
		
		s = fstream[4].split("= ")
		existing_size = int(s[1].strip("\n"))
		#-15 from current result to compensate for adding Filesize details 15bytes
		current_size = os.stat("settings.txt").st_size - 15
		if existing_size <  current_size or  existing_size > current_size:
			
			print "** Settings file corrupt, file may have been modified manually"
			return False
		else:
			return True
	else:
		return False
		
