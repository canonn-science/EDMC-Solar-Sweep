# -*- coding: utf-8 -*-
import sys
import re
import ttk
import Tkinter as tk
import requests
import os
from urllib import quote_plus
from  math import sqrt,pow,trunc
from ttkHyperlinkLabel import HyperlinkLabel
from config import applongname, appversion
import myNotebook as nb
from config import config


this = sys.modules[__name__]
this.s = None
this.prep = {}
this.debuglevel=3

# Lets capture the plugin name we want the name - "EDMC -"
myPlugin = "Solar-Sweep"

class Sweeper:

	def __init__(self,parent):
		debug("Initiating Solar Sweep")
		self.completed={}
		self.parent=parent
		
	def fsdJump(self,cmdr, system, station, entry):
		self.cmdr=cmdr
		self.system=system
		self.setStatus(self.system,entry["StarPos"][0],entry["StarPos"][1],entry["StarPos"][2])	
		
			
	def cmdrData(self,data):
		debug(data,2)
		self.cmdr=data["commander"]["name"]
		self.system=data["lastSystem"]["name"]
		x,y,z = edsmGetSystem(self.system)
		self.setStatus(self.system,x,y,z)
		
			
	def Location(self,cmdr, system, station, entry):		
		self.cmdr=cmdr
		self.system=system
		debug("Setting Location",2)
		self.setStatus(self.system,entry["StarPos"][0],entry["StarPos"][1],entry["StarPos"][2])
		
				
	def setStatus(self,system,x,y,z):
		if getDistanceSol(x,y,z) <= 200:
			#self.completed["Merope"]=True
			self.getSystems()
			this.frame.grid()
			
			try:
				if self.completed[system]==True:
					this.status["width"]=200
					this.status["width"]=self.parent.winfo_width()-10
					this.status["text"]="This system has been fully surveyed"
					#this.url["text"]="Report to Canonn"
					#this.url["url"]="https://docs.google.com/forms/d/e/1FAIpQLSe1rXxMX0sML3EH0At-_mr-KZrJrj4EdhY0o-o9O0UJ7CoyLg/viewform?usp=pp_url&entry.593288406="+quote_plus(this.system)+"&entry.273955456="+quote_plus(this.cmdr)+"&entry.543965287=No&entry.1149469095=No"
					this.status.grid()
					this.url.grid_remove()
			except:
				this.status["text"]="Fly within 1000ls of each body and log any points of interest."	
				this.status["width"]=200
				this.status["width"]=self.parent.winfo_width()-10				
				this.url["text"]="Report to Canonn"
				sys=quote_plus(self.system)
				cmd=quote_plus(self.cmdr)
				this.url["url"]="https://docs.google.com/forms/d/e/1FAIpQLSe1rXxMX0sML3EH0At-_mr-KZrJrj4EdhY0o-o9O0UJ7CoyLg/viewform?usp=pp_url&entry.593288406="+sys+"&entry.273955456="+cmd+"&entry.543965287=No&entry.1149469095=No"
				this.label.grid()
				this.status.grid()
		else:
			this.status.grid_remove()
			this.label.grid_remove()
			this.url.grid_remove()
			this.frame.grid_remove()
			
	def getSystems(self):
		#get list of completed systems
		
		url="https://docs.google.com/spreadsheets/d/e/2PACX-1vStWhpR7K4VpiFMwLNOqCeC4Fl9mLC8DdXhTSq5Kd0Jwv0oimO3TpgKRZd6NiwtjwurqPXAieBw1pe0/pub?gid=1120799764&single=true&output=csv"
		r = requests.get(url)
		for line in r.content.split("\n"):
			a = []
			a = line.split(",")
			self.completed[a[0].rstrip()]=True
			debug(a[0].rstrip(),3)
			
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
	this.frame = tk.Frame(parent)
	
	
	
	this.frame = tk.Frame(parent)
	this.frame.columnconfigure(2, weight=1)
	
	this.label = tk.Label(this.frame, text= myPlugin + ":")
	this.status = tk.Message(this.frame,width=0, anchor=tk.W, text="Ready")
	this.url=HyperlinkLabel(this.frame, compound=tk.RIGHT, popup_copy = True)
	
	this.label.grid(row = 0, column = 0, sticky=tk.W)	
	this.url.grid(row = 0, column = 1, sticky=tk.W)
	
	this.status.grid(row = 1, column = 0, columnspan=2, sticky=tk.W)
	
	this.label.grid_remove
	this.status.grid_remove
	this.url.grid_remove
	
	
	
	##this._CARTO = tk.PhotoImage(file = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))+'/carto.gif')
	##label["image"]=this._CARTO
	
	this.sweep = Sweeper(parent)
	return (this.frame)

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
	

