#!/usr/bin/env python
#coding=utf-8

import fbchat
import schedule
import time
import os
import random
import datetime
import password
from fbchat import log, Client
from fbchat.models import *

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'pos.txt')
my_polse = os.path.join(THIS_FOLDER, 'polser.PNG')


#Different often used global variables
Room_position = 12
day_counter = 2
days_between_each_trash_day = 3
Washing_week_position = 7

current_residents = ["Jonas","Hanne","Kristianne","Sabine","Inga","away","Thomas","away","Jostein","away","away","Sivert","Benjamin","away","away"]
number_of_rooms = len(current_residents)


#Thread to post Garbage/Washing updates in
main_thread_id = "2604038489700339" #Kollektivchat
main_thread_type = ThreadType.GROUP


list_of_msgs_part_1 = [u'It\'s that time of month ',
u'Guess what ',
u'I don\'t want to say this ',
u'Friendly reminder ',
u'Oopsie ',
u'Good news?? Or maybe bad news for ',
u'Hey you ',
u'Hope you are alright ',
u'']

list_of_msgs_part_2 = [u', the trash is all yours today ',
u', looks like you have to take out the trash today ',
u', take out them bins! ',
u', the bags with the trash, you know what to do ',
u', it smells in the kitchen, take out those bags ',
u', would you be so polite as to take those bags of waste and toss them in the containers outside? ']

list_of_thread_colours = [ThreadColor.RUBY]

list_of_emojis = [u'🤣', u'😇', u'🤭', u'😬', u'😷', u'🤯', u'🥙', u'🍲', u'🦄',u'🥵',u'🥴',u'🤠',u'🤓',u'😎',u'😱',u'🤬',u'💩',u'👺',u'👻',u'👽',u'💘',u'💦',u'🤙',u'👊',u'👀']




#Extra used for debugging:
#thread_id_own = client.uid
#thread_type_own = ThreadType.USER





class Soppelbot(Client):
	def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
		message_list = message_object.text.split()
		time.sleep(1)
		for word in message_list:
			word.strip()
		if((message_list[0].decode('utf-8').lower()) == "help"):
			self.reactToMessage(message_object.uid, MessageReaction.SMILE)
			text= "Here are a list of commands:\n\"help\"\n\"add <name> <number>\"\n\"remove <number>\"\n\"print all rooms\"\n\"pls poelser\" " + random.choice(list_of_emojis)
			self.send(Message(text=text), thread_id=thread_id, thread_type=thread_type)
		if((message_list[0].decode('utf-8').lower()) == "add"):
			self.reactToMessage(message_object.uid, MessageReaction.HEART)
			
			try:
				room_number = int(message_list[-1])
				if(room_number > number_of_rooms):
					self.send(Message(text="There aren't that many rooms in this collective"), thread_id=thread_id, thread_type=thread_type)
					return
			except ValueError:
				self.send(Message(text="Wrong syntax: add <name> <room number>"), thread_id=thread_id, thread_type=thread_type)
				return
			
			if(message_list[1].isdigit()):
				self.send(Message(text="It has to be a name not a number. Syntax: add <name> <room number>"), thread_id=thread_id, thread_type=thread_type)
				return
			room_number = int(message_list[-1])
			name = " "
			name = name.join(message_list[1:-1]).decode('utf-8', 'ignore')
			if(current_residents[room_number-1] == 'away'):
				current_residents[room_number-1] = name.title()
				self.send(Message(text="Welcome " + current_residents[room_number-1] + "! " + random.choice(list_of_emojis)),  thread_id=thread_id, thread_type=thread_type)
				print(current_residents)
			else:
				self.send(Message(text="That room is already occupied by: " + current_residents[room_number-1]),  thread_id=thread_id, thread_type=thread_type)
		if(message_list[0].decode('utf-8').lower() == "remove" and len(message_list) == 2):
			self.reactToMessage(message_object.uid, MessageReaction.HEART)
			room_number = int(message_list[1])
			old_resident = current_residents[room_number-1]
			current_residents[room_number-1] = 'away'
			self.send(Message(text="Room number " + str(room_number) + " is now set as away. See you next time " + old_resident + "! " + random.choice(list_of_emojis)),  thread_id=thread_id, thread_type=thread_type)
		
		if(message_list[0].decode('utf-8').lower() == "print" and message_list[1].decode('utf-8').lower() == "all" and message_list[2].decode('utf-8').lower() == "rooms"):
			self.reactToMessage(message_object.uid, MessageReaction.HEART)
			final_text = ""
			for a in range(len(current_residents)):
				final_text += "| " + str(a+1) + " - " + current_residents[a] + "\n"
			self.send(Message(text=final_text), thread_id=thread_id, thread_type=thread_type)
		
		if(message_list[0].decode('utf-8').lower() == "pls" and message_list[1].decode('utf-8').lower() == "poelser"):
			self.reactToMessage(message_object.uid, MessageReaction.LOVE)
			self.sendLocalImage(
				my_polse,
				message=Message(text="Pølser er registrert om 15"),
    			thread_id=thread_id,
    			thread_type=thread_type,
			)

		else:
            # Sends the data to the inherited onMessage, so that we can still see when a message is recieved
			super(Soppelbot, self).onMessage(
				author_id=author_id,
				message_object=message_object,
				thread_id=thread_id,
				thread_type=thread_type,
				**kwargs
            )


def updateSoppelDag():
	global day_counter
	global Room_position

	if(day_counter == days_between_each_trash_day):
		while(current_residents[Room_position] == 'away'):
			Room_position += 1
			if(Room_position > len(current_residents)-1):
				Room_position = 0
		text = random.choice(list_of_msgs_part_1) + current_residents[Room_position] + random.choice(list_of_msgs_part_2) + random.choice(list_of_emojis)
		day_counter = 0
		Room_position += 1

		client.send(Message(text=text), thread_id=main_thread_id, thread_type=main_thread_type)

		if(Room_position > len(current_residents)-1):
			Room_position = 0
	day_counter += 1

	print("Day: " + str(day_counter))
	print("Room_position: "+ str(Room_position))


def updateWashingWeek():
	global Washing_week_position
	washing_list = []
	for i in range(3):
		if(Washing_week_position>number_of_rooms-1): 
				Washing_week_position = 0
		while(current_residents[Washing_week_position] == 'away'):
			Washing_week_position += 1
			if(Washing_week_position>number_of_rooms-1): 
				Washing_week_position = 0
		washing_list.append(current_residents[Washing_week_position])
		Washing_week_position += 1
	text = "The current washing-roster: " + washing_list[0] + ", " + washing_list[1] + " and " + washing_list[2] + ". Remember to wash today " + random.choice(list_of_emojis)
	client.send(Message(text=text), thread_id=main_thread_id, thread_type=main_thread_type)
	print("Washing_week_position: " + str(Washing_week_position))




#Starting the bot
client = Soppelbot('soppelbot@gmail.com', password.password)
#client.setDefaultThread(thread_id, thread_type)


#schedule.every().day.at("13:00").do(updateSoppelDag)
#schedule.every(0.1).minutes.do(updateSoppelDag)
#schedule.every(0.1).minutes.do(updateWashingWeek)

schedule.every().sunday.at("10:00").do(updateWashingWeek)
schedule.every().day.at("12:00").do(updateSoppelDag)


#Main Loop
while(True):
	schedule.run_pending()
	client.setActiveStatus(markAlive=True)
	client.startListening()
	client.doOneListen()

	time.sleep(1)

	
