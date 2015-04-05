#!/usr/bin/python
import sys,os,time
sys.path.append('/home/graham/Documents/py')
import settings, email_client_tls as client
import platform as arch
import security as secure

start = """
 ______   __  __     ______     __    __     ______     __     __           
/\  == \ /\ \_\ \   /\  ___\   /\ "-./  \   /\  __ \   /\ \   /\ \          
\ \  _-/ \ \____ \  \ \  __\   \ \ \-./\ \  \ \  __ \  \ \ \  \ \ \____     
 \ \_\    \/\_____\  \ \_____\  \ \_\ \ \_\  \ \_\ \_\  \ \_\  \ \_____\    
  \/_/     \/_____/   \/_____/   \/_/  \/_/   \/_/\/_/   \/_/   \/_____/    
                      
     PyEmail - Simple and easy to use comand line smtp over tls client 
               By Graham Murray 2015 www.graham-murray.com             
                                                                                                                         
		"""
def clearscr():
	if arch.system() == 'Linux' or arch.system() =='Linux2' or arch.system() =='Linux3':
		print 'linux'
		os.system('clear')
	elif arch == 'darwin':
		print 'OS X'
		os.system('clear')
	elif archsystem() == 'Windows':
		print 'Windows'
		os.system('cls')
		
	
clearscr()
print start
result = settings.check_settings()

def dump_settings():#Perform all actions required to generate settings.txt
	details= settings.set_settings()	
	host = details[0]
	port = details[1]
	sender = details[2]
	
	
	detailsobj = settings.verify_account(host,port,sender)
	success_of_record = settings.set_settings_file(detailsobj)
	return success_of_record
	
def options_init(option):
	if option == '1':
		#New Email		
		message = client.create_email()
		
		if message == False:
			options_init(option)
		else:
			#this will need to populate email object and pass detailsobj and message in tp email class and the pass full email to be sent
			to_addr = message[0]
			subj = message[1]
			msg_body = message[2]

			#This be of type detailsobj with futher developement
			detailsobj = settings.load_settings()
			host = detailsobj[0]
			port = detailsobj[1]
			sender = detailsobj[2]
			username = detailsobj[3]
			
			
			email = client.email(host,port,sender,to_addr,username,subj,msg_body)
			client.send_email(email)
			
			time.sleep(2)
			

			logger = secure.log(email)
			logger.write_log()
			clearscr()
			print start
			enter_options()
			
	elif option == '2':
		#Reset settings
		success_of_record = dump_settings()
		if success_of_record == '1':
			option = enter_options()
			
		else:
			exit("Error writing settings, please try again")
	else:
		if option == '3':
			print "PGP support coming soon"
		elif option == '4':
			exit("Bye!")
		else:
			print "Option must be either 1,2,3 or 4"
			
if result == False:
	print "Please complete the following details"
	dump_settings()
else:
	settings_package = settings.load_settings()

	#details for sending email
	host = settings_package[0]
	port = settings_package[1]
	sender = settings_package[2]
	username = settings_package[3]

def enter_options():

	option = raw_input("\n\tOptions\n\t1: New Email\t\t2: Reset Settings\n\t3: Encrpyted PGP Email\t4: Quit\n\nPlease enter an option @> ")
	
	options_init(option)
	return option

enter_options()
	

