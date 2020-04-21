#!/usr/bin/env python2
#coding=utf-8

import fbchat

from fbchat import Client
from fbchat.models import *
client = Client('soppelbot@gmail.com', 'Soppel123') 

people = ["Sivert", "Benjamin", "Jonas", "Hanne", "Kristianne", "Sabine", "Inga", "Thomas", "Jostein"]


daysBetweenEachMsg = 3
thread_id = "1965858186869179"
thread_type = ThreadType.GROUP

pos = 0


with open('/home/borge/Documents/Bot/pos.txt', 'r') as f:
	tekst = f.read()
	tekst.strip()
	tekst_list = tekst.split(",")
	pos = int(tekst_list[0])
	dagCounter = int(tekst_list[1])
	print(pos)
	print(dagCounter)



	if(dagCounter == daysBetweenEachMsg):
		text = "Det er i dag " + people[pos] + " sin tur til å ta ut søpla. God tur :)"
		dagCounter = 0
		pos += 1

		client.send(Message(text=text), thread_id=thread_id, thread_type=thread_type)

		if(pos > len(people)-1):
			pos = 0


dagCounter += 1

with open('/home/borge/Documents/Bot/pos.txt', 'w') as f:
	f.write(str(pos))
	f.write(",")
	f.write(str(dagCounter))



client.logout()
