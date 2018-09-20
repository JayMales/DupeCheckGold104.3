#!/usr/bin/env python

import requests
from lxml import html
import json, time, datetime


class Songs:
	def __init__(self, songName, artist, played_datetime):
		self.sN = songName
		self.a = artist
		self.pd = played_datetime
		
	def checkForDupe(self,songName,artist):
		if songName == self.sN and artist == self.a:
			return True
		else:
			return False
			
	def text(self):
		bla = "Gold FM has now played "+self.sN+" by: " +self.a+" twice. The first time they played it was: "+self.pd+ " call: 9414 1043"
		return bla
	
def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except:
        return False
		
def send_text(song):
	s = requests.Session()
	s.auth = ('476ba368d1ab6ed301f313f0263daf6e', 'test')
	task = {'message': song.text(), "to": ""}
	s.post('https://api.transmitsms.com/send-sms.json', data=task)
	
if __name__ == '__main__':
	print "Gold FM bot as started"
	clean = open("listOfDataClean.txt",'a') 
	dirty = open("listOfDataDirty.txt",'a') 
	listOfSongs = []
	prevA = ""
	prevS = ""
	try:
		while True:
			#now = datetime.datetime.now()
			#today6am = now.replace(hour=6, minute=0, second=0, microsecond=0)
			#today6pm = now.replace(hour=18, minute=0, second=0, microsecond=0)
			#if today6am > now and today6pm < now:
			#	time.sleep(60)
			#else:
				page = requests.get('http://media.arn.com.au/XML-JSON.aspx?source=http://www.gold1043.com.au&feedUrl=/xml/gold1043_now.xml')
				try:
					artist = page.json()["on_air"]["previously_played"]["audio"][0]["artist"]["value"]
					songName = page.json()["on_air"]["previously_played"]["audio"][0]["title"]["value"]
					played_datetime = page.json()["on_air"]["previously_played"]["audio"][0]["played_datetime"]["value"] 
					if artist != prevA and songName != prevS:
						prevA = artist
						prevS = songName
						if prevA != "Gold 104.3" and prevS != "Better Music and More of It":
							clean.write(artist+" - "+songName+" - Played at: "+played_datetime+"\n")
							dirty.write(json.dumps(page.json(),ensure_ascii=False)+"\n")
							print artist+" - "+songName
							
							for song in listOfSongs:
								if song.checkForDupe(songName,artist):
									send_text(song)
							listOfSongs.append(Songs(songName,artist,played_datetime))
				except ValueError:
					print "object was empty"
					time.sleep(20)
				else:
					time.sleep(80)
	finally:
		clean.close()
		dirty.close()
		print "error and closed"
		
