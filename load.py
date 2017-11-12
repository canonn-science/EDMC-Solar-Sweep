# -*- coding: utf-8 -*-
import sys
import re
import ttk
import Tkinter as tk
import requests
import os
from urllib import quote_plus
from  math import sqrt,pow,trunc

from config import applongname, appversion
import myNotebook as nb
from config import config


this = sys.modules[__name__]
this.s = None
this.prep = {}
this.debuglevel=2

# Lets capture the plugin name we want the name - "EDMC -"
myPlugin = "Solar-Sweep"

class Sweeper:

	def __init__(self,frame):
		debug("Initiating Solar Sweep")
		self.completed={}
		
	def fsdJump(self,cmdr, system, station, entry):
		self.arrival=entry["timestamp"].replace("T"," ").replace("-","/").replace("Z","")
		self.sysx=entry["StarPos"][0]
		self.sysy=entry["StarPos"][1]
		self.sysz=entry["StarPos"][2]
		# need to set this so we know we have coordinates available
		self.jumped=True
		if getDistanceSol(self.sysx,self.sysy,self.sysz):
			this.status["text"]="in range"
			getSystems()
			if completed(system)==True:
				this.status["text"]="This system has been fully surveyed"
		else:
			this.status["text"]="out of range"
			
	def cmdrData(self,data):
		debug(data,2)
		x,y,z = edsmGetSystem(data["lastSystem"]["name"])
		self.sysx=x
		self.sysy=y
		self.sysz=z
		if getDistanceSol(self.sysx,self.sysy,self.sysz):
			this.status["text"]="in range"
			getSystems()
			if completed(system)==True:
				this.status["text"]="This system has been fully surveyed"
		else:
			this.status["text"]="out of range"
			
	def Location(self,cmdr, system, station, entry):		
		debug("Setting Location",2)
		self.sysx=entry["StarPos"][0]
		self.sysy=entry["StarPos"][1]
		self.sysz=entry["StarPos"][2]
		if getDistanceSol(self.sysx,self.sysy,self.sysz):
			this.status["text"]="in range"
			getSystems()
			if completed(system)==True:
				this.status["text"]="This system has been fully surveyed"
		else:
			this.status["text"]="out of range"		
				
		
	def getSystems(self):
		#get list of completed systems
		
		url="https://docs.google.com/spreadsheets/d/e/2PACX-1vStWhpR7K4VpiFMwLNOqCeC4Fl9mLC8DdXhTSq5Kd0Jwv0oimO3TpgKRZd6NiwtjwurqPXAieBw1pe0/pub?gid=1120799764&single=true&output=csv"
		r = requests.get(url)
		s =  r.json()
		for line in r.content.split("\n"):
			a = []
			a = line.split(",")
			self.completed[a[0]]=True
			
def debug(value,level=None):
	if level is None:
		level = 1
	if this.debuglevel >= level:
		print "["+myPlugin+"] "+str(value)

def edsmGetSystem(system):
	url = 'https://www.edsm.net/api-v1/system?systemName='+quote_plus(system)+'&showCoordinates=1'		
	#print url
	r = requests.get(url)
	s =  r.json()
	#print s
	return s["coords"]["x"],s["coords"]["y"],s["coords"]["z"]
		
def plugin_start():
	"""
	Load Template plugin into EDMC
	"""
		
	print myPlugin + "Loaded!"
	
	return myPlugin

def getDistanceSol(x,y,z):
	return round(sqrt(pow(float(x),2)+pow(float(y),2)+pow(float(z),2)),2)

def plugin_app(parent):
	label = tk.Label(parent, text= myPlugin + ":")
	this.status = tk.Label(parent, anchor=tk.W, text="Ready")
	
	this.sweep = Sweeper(parent)
	return (label, this.status)

# Log in


# Detect journal events
def journal_entry(cmdr, system, station, entry):

		
	if entry['event'] == 'FSDJump':
							
		this.sweep.fsdJump(cmdr, system, station, entry)
	
	if entry['event'] == 'Location':
		this.sweep.Location(cmdr, system, station, entry)
		
	if entry['event'] == 'StartUp':
		this.sweep.startUp(cmdr, system, station, entry)		

# Update some data here too
def cmdr_data(data):
	this.sweep.cmdrData(data)
	

