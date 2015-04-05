#!/usr/bin/python

import smtplib,sys
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
sys.path.append('/home/graham/Documents/py')
import security as secure
import os

class email:
	def __init__(self,host,port,sender,reciever,username,subject,message):
		self.host = host
		self.port = port
		self.sender = sender
		self.reciever = reciever
		self.username = username
		self.subject = subject
		self.message = message
		
def create_email():
	EMAIL_TO = raw_input("Enter a recipient @> ")
	if not secure.check_email(EMAIL_TO):
		print "** Incorrect email format 'someone@domain.com' **";
		return False;
	EMAIL_SUBJECT = raw_input("Please enter a subject @> ")

	msg_body = raw_input("Enter a message @> ")
	mesg = [EMAIL_TO,EMAIL_SUBJECT,msg_body]
	return mesg


	
def send_email(email): 
	os.system("stty -echo")
	SMTP_PASSWORD = raw_input("Account Password: ")
	os.system("stty echo")
	msg = MIMEMultipart()
	part = MIMEText(email.message)
	msg.attach(part)
	msg['Subject'] = email.subject
	msg['From'] = email.sender
	msg['To'] = email.reciever
	part = MIMEApplication(open("/home/graham/Documents/py/settings.txt","rb").read())
	part.add_header('Content-Disposition','attachment',filename="settings.txt")
	msg.attach(part)
	debuglevel = True
	mail = smtplib.SMTP(email.host, email.port)
	mail.set_debuglevel(debuglevel)
	mail.starttls()
	mail.login(email.username, SMTP_PASSWORD)
	mail.sendmail(email.sender, email.reciever, msg.as_string())
	mail.quit()
    
