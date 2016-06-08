# # # # # # # # # # # # # # # # #
#	Self-Care Bot 0.3a		#
#	Designed by Kelly Maere		#
#	Programmed by Colin Diener	#
# # # # # # # # # # # # # # # # #

"""
TODO:	Update code to reflect new Telegram API 2.0
		Update code to reflect new version of telepot
		Remove threading, replace with asynchronous calling
"""

import telepot
from datetime import datetime, time
from time import sleep
from random import randint
import emoji
# To ask people at the same time
import threading
try:
	from ConfigParser import SafeConfigParser
except:
	from configparser import *
import json

# Get the API key
parser = SafeConfigParser()
parser.read('settings.ini')
api = parser.get('scb_settings', 'api_key')

# Create the Bot, global vars
bot = telepot.Bot(api);
bot.setWebhook()
users = json.loads(parser.get("users","toImport"))
userreply = []
meduser = json.loads(parser.get("users","medUsers"))

runToday = False
# We're good to go!
print('SCB is up and running, adding users to base...')

# Enter their last response
for i in users:
	userreply.append(0)

# Messages
greeting = []
water = []
otherdrink = []
eat_yes = []
eat_no = []
med_yes = []
med_no = []
bye = []

greeting.append("Just checking in! Have you eaten today?")
greeting.append("Howdy! You've eaten already, right?")
greeting.append("Hey there! Have you eaten?")
greeting.append(emoji.emojize(":smile: Hello~ Have you eaten today?", use_aliases=True))
water.append("Great! Don't forget to drink enough!")
water.append("That's fantastic, I'm proud of you :)")
water.append("Look at you! You're doing great!")
water.append("Nice! Don't forget to stay hydrated!")
otherdrink.append("That's fine, but you should have some water, too!")
otherdrink.append("That's alright, don't forget to have some water!")
otherdrink.append("You should go have a glass of water while you're thinking of it!")
otherdrink.append("Alright... Don't forget to have some water~")
eat_yes.append(emoji.emojize(":strawberry: Great!", use_aliases=True))
eat_yes.append(emoji.emojize("Good! You're doing great :ok_hand:", use_aliases=True))
eat_yes.append("Remember to eat healthy! You're doing great :)")
eat_yes.append("That's fantastic, keep it up!")
eat_no.append("You really should eat something. Maybe go get something now while you're thinking of it?")
eat_no.append("Home cooking is a cheap alternative to eating out, and it's fun! You should try it!")
eat_no.append("Please do! I love you and want you to be healthy and strong!")
eat_no.append("Aw :( Please eat something... for me?")
med_yes.append(emoji.emojize(":pill: Way to go!", use_aliases=True))
med_yes.append(emoji.emojize(":thumbsup: Good!", use_aliases=True))
med_yes.append("That's great!")
med_yes.append("I'm so proud of you :)")
med_no.append(":( Please take them, they're there to help you and we love you and we don't want you to get hurt somehow...")
med_no.append("Don't forget to take them... We don't want something to happen to you...")
med_no.append("Remember that we love you and we care about you, and that you should take them...")
med_no.append("Hey! Take them! I care about you and I want you to be okay!")
bye.append(emoji.emojize("Alright :revolving_hearts: Don't forget to take care of yourself! You're super important to us :blush:", use_aliases=True))
bye.append("You're doing great. Don't forget, we're all super proud of you and we love you :) See you tomorrow!")
bye.append("I'm so proud of you! Don't forget to take care of yourself <3")
bye.append(emoji.emojize("Alright :revolving_hearts: Don't forget to take care of yourself! You're our sunshine :sunny:", use_aliases=True))
print('All set. Executing...')

# Threading to send to different people!
class ThreadingObj(threading.Thread):
	def __init__(self, id):
		threading.Thread.__init__(self)
		self.id = id

	def run(self):			#lmao what am I even doing
		checkup(self.id, self)	#what is this, what is you?

# Function that will actually send the messages
# userid is going to be the person it sends it to
def checkup(counter, thisthread):
	no = {'hide_keyboard': True}
	yesno = {'keyboard': [['Yes','No']]}
	drinks= {'keyboard': [['Water','Tea'],['Coffee','Soda','Nothing/Other']]}
	started = datetime.now()
	bypass = False
	def checkKill():
		delta = datetime.now() - started
		if delta.total_seconds() > 72000:	# 72000 seconds is 20 hours
#		if delta.total_seconds() > 10:
			bypass = True
			userreply[counter] = 0

	userid = users[counter];
	userreply[counter] = 0 # In case they messaged it in between or something
	delay = 1		# So that my computer doesn't explode constantly checking

	bot.sendMessage(userid, greeting[randint(0,3)], reply_markup=yesno)
	while (userreply[counter] == 0 and bypass == False):
		sleep(delay)
		checkKill()
	if bypass == False:
		if userreply[counter] == 'Yes':
			bot.sendMessage(userid, eat_yes[randint(0,3)], reply_markup=no)
		if userreply[counter] == 'No':
			bot.sendMessage(userid, eat_no[randint(0,3)], reply_markup=no)
		userreply[counter] = 0

		bot.sendMessage(userid, "What have you had to drink?", reply_markup=drinks)
	
	while (userreply[counter] == 0 and bypass == False):
		sleep(delay)
		checkKill()
	if bypass == False:
		if userreply[counter] == 'Water':
			bot.sendMessage(userid, water[randint(0,3)], reply_markup=no)
		if userreply[counter] == 'Tea' or userreply[counter] == "Soda" or userreply[counter] == 'Coffee':
			bot.sendMessage(userid, otherdrink[randint(0,3)], reply_markup=no)
		if userreply[counter] == 'Nothing/Other':
			bot.sendMessage(userid, "Don't forget to hydrate with some water!", reply_markup=no)
		userreply[counter] = 0
		# This is below a bypass statement because it will skip both if bypass is true
		if userid in meduser:
			bot.sendMessage(userid, "Are you taking your medications?", reply_markup=yesno)
			while (userreply[counter] == 0 and bypass == False):
				sleep(delay)
				checkKill()
			if bypass == False:			
				if userreply[counter] == "Yes":
					bot.sendMessage(userid, med_yes[randint(0,3)], reply_markup=no)
				if userreply[counter] == "No":
					bot.sendMessage(userid, med_no[randint(0,3)], reply_markup=no)
	
	userreply[counter] = 0 		# Just in case <3

	# Bye!
	bot.sendMessage(userid, bye[randint(0,3)], reply_markup=no)

def setup():
	parser.read('settings.ini')
	users = json.loads(parser.get("users","toImport"))
	del userreply[:]
	meduser = json.loads(parser.get("users","medUsers"))
	for i in users:
		userreply.append(0)
	print("User list updated, all set to go.")
def runme():
	print('Creating threads, asking questions...')
	usercount = 0
	for i in users:
		thread = ThreadingObj(usercount)
		usercount = usercount+1
		thread.start()

def writeConfig():
	parser.set('users','toImport', json.dumps(users))
	parser.set('users','medUsers', json.dumps(meduser))
	# Now that we've made the modifications, write to file
	with open('settings.ini','w') as configfile:
		parser.write(configfile)

def handle(msg):
	chat_id = msg['chat']['id']
	command = msg['text']

	if chat_id in users:
		if '/broadcast' in msg['text']:
			bmsg = msg['text']
			bmsg = bmsg[10:]
			for i in users:
				bot.sendMessage(i,bmsg)
		userreply[users.index(msg['chat']['id'])] = msg['text']

	if '/rem' in msg['text']:
		userreply.pop(users.index(msg['chat']['id']))
		users.remove(chat_id)
		# For good measure!
		meduser.remove(chat_id)
		writeConfig()
		print("%s has opted out of the SCB service." % chat_id)
		bot.sendMessage(chat_id,"Sorry to see you go. I won't contact you any more. Send me /start if you change your mind<3")
	if '/start' in msg['text']:
		if chat_id not in users:
			userreply.append(0)
			users.append(chat_id)
			writeConfig()
			print("%s has opted into the SCB service." % chat_id)
			bot.sendMessage(chat_id,"Hi! You've been added to my list of people to contact everyday. You can send me /rem if you no longer wish to recieve messages. Send me /med if you wish to be asked about medications each day.")
	if '/med' in msg['text']:
		meduser.append(chat_id)
		writeConfig()
		bot.sendMessage(chat_id,"I'll ask you if you've taken your meds each day :)")


# Listen for commands
bot.message_loop(handle)

# This loop will run forever
while True:
	now = datetime.now()
	now_time = now.time()
	if now_time >= time(14,00) and now_time <= time(17,00) and runToday is False:
		setup()
		runme()					# Call the real function
		runToday = True
	if now_time >= time(20,00) and now_time <= time(23,00):
		runToday = False
	sleep(7200)		# There are 7200 seconds in 2 hours
