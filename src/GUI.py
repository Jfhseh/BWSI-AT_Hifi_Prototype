"""
**Note:**
{SERVER_URL} is deleted from the code
"""
###### Import Statements #######
from tkinter import *;         # for GUI
import time;import os;         #
import json;               		 # 
from PIL import ImageTk, Image # regular tkinter image only supports .png										 
from pygame import mixer;      # is .wav better for pygame than mp3?
################################
#from playsound import playsound;
from google_drive_downloader import GoogleDriveDownloader as gdd;
import screen_brightness_control as sbc;
import requests;
DELETE_USED = True;
HAVE_DISPLAY = False;
CAN_QUIT_APP = True;
NOLOAD_WHEN_EXIST = True;
########## initialize app and variables ###############################
mixer.init();                                                         # initialize music player
TIME_REMINDER_FONT = ("Oswald", 20, "bold");                          # set up fonts
REMINDER_FONT = ("Oswald", 15, "normal");                             #
root = Tk();                                                          #
#root.wm_attributes('-fullscreen', 'True');                           # 
screenW:int = 200;                                                    # 
screenH:int = 200;                                                    #
frm = Frame(root);                                                    # set up window
root.configure(highlightthickness=0,background='#b8faff');            #
frm.grid();                                                           #
root.geometry(str(screenW)+"x"+str(screenH));                         #
timeLabel = Label(frm, text="Loading Time...", font = TIME_REMINDER_FONT); # Label that shows time
timeLabel.configure(bg='#b8faff', foreground = "black");              #
timeLabel.pack();                                                     #
#######################################################################
#################  Reminder Label  #######################################################
reminderLabel = Label(root, text="Loading Data...");                                     #
photo =  ImageTk.PhotoImage(Image.open("001.jpg").resize((60, 60)));#TODO: change this to#
# photo = photo.subsample(int(photo.width() / 60+0.5));                                  #
reminderLabel.place(x=screenW/2-80,y=screenH/2-60);                                      #
reminderLabel.configure(bg='#b8faff', foreground = "black", font = REMINDER_FONT);       #
# reminderLabel.pack(padx=0,pady=0);																										 #
################  Image Label  ###########################################################
imageLabel = Label(root, text="hi",image = photo);																	 		 #
imageLabel.place(x=screenW/2+10,y=screenH/2-40);																				 #
imageLabel.configure(bg='#b8faff', foreground = "black");																 #
##########################################################################################
def exitApp():
	root.destroy();
exitButton = Button(root,text ='exit app', command = exitApp);
exitButton.place(x=screenW/2-80,y=screenH/2);																				 
exitButton.configure(bg='#b8faff', foreground = "black");
repeatBtn = Button(root,text ='Repeat'); #configed in Main.setup
repeatBtn.place(x=screenW/2-80,y=screenH/2+40);																				 
repeatBtn.configure(bg='#b8faff', foreground = "black");
reminders = {"":""};
month = time.localtime().tm_mon;
date = time.localtime().tm_mday;
class BrightnessManager:
	@staticmethod
	def setBrightness(percent):
		if not HAVE_DISPLAY:
			return;
		sbc.set_brightness(percent);
	@staticmethod
	def batterySave():
		"""reset display brightless _**if**_ the device is left 3min idle"""
		if not HAVE_DISPLAY:
			return;
		if (time.time() - Main.lastTimeChecked < 180):
			return;
		BrightnessManager.setBrightness(5);
		
class GoogleDriveManager:
	text = "";
	@staticmethod
	def getSchedule():
		print("GoogleDriveManager: getting schedule");
		currentFolder = f'./data/{month}-{date}/';
		#vv need to be changed if appscript version changed
		x = requests.get('{INSERT SERVER URL HERE}');
		print(x.status_code);
		print(x.text);
		#^^automatically close the file 
		GoogleDriveManager.text = x.text;
	@staticmethod
	def download(fileID, fileExtension, time):
		file = str(month)+"-"+str(date)+"-"+time+fileExtension;
		dest = f"./data/{month}-{date}/{file}";
		gdd.download_file_from_google_drive(fileID, dest);
		return dest[2:];
class Reminder:
	@staticmethod
	def parse(data:str):
			global reminders;
			data = json.loads(data);
			for key in data.keys():
					if (type(data[key]) == dict):
							data[key]['time'] = key;
							reminders[key] = Reminder.new(data[key]);
	time = "0:00";
	text = "reminder";
	audio = None;
	imgSrc = None;
	img = None;
	def new(data:dict):
		this = Reminder("","");
		for (i,val) in data.items():
				if i == 'time':
						this.time = val;
				elif i == 'text':
						this.text = val;
				elif i == 'audioSrc':
						this.audio = GoogleDriveManager.download(val, data['audioSrcExtension'],data['time']);
				elif i == 'imageSrc':
						this.imgSrc = GoogleDriveManager.download(val, data['imageSrcExtension'], data['time']);
		return this;
	def __init__(this, time, text, audio=None, imgSrc = None):
		this.time = time;
		this.text = text;
		this.audio = audio;
		this.imgSrc = imgSrc;
	def show(this):
		reminderLabel.configure(text= this.text, bg = "#8aff78");
		Main.checkedNewReminder = False;
		#TODO: add new reminder FX
		if (this.audio != None):
			print(this.audio);
			Speaker.play(this.audio);
		if (this.imgSrc != None):
			imageLabel.configure(image = this.loadImage());
	def loadImage(this):
		if this.img != None:
			return this.img;
		this.img = ImageTk.PhotoImage(Image.open(this.imgSrc).resize((60, 60)));
		return this.img;
#TODO: setup raspberry pi speaker
class Speaker:
	@staticmethod 
	def setup():
		pass;
	
	@staticmethod
	def play(fileName:str):
		mixer.music.load("newReminder.wav");
		mixer.music.play(1);
		def after():
			mixer.music.load(fileName);
			mixer.music.play(1);
		root.after(2001,after);
		# playsound(fileName,False);
		print("Playing audio");			

def formatTime(currentDateTime):
    currentDateTime = time.localtime();
    hr = str(currentDateTime.tm_hour);
    min = str(currentDateTime.tm_min);
    if (len(hr) == 1):
        hr = "0"+hr;
    if (len(min) == 1):
        min = "0"+min;
    return hr+":"+min;
	
#TODO: delete return
def loadReminders():	
	currentFolder = f'./data/{month}-{date}/';
	if NOLOAD_WHEN_EXIST and os.path.exists(currentFolder):
		print('already loaded :D');
		with open(currentFolder+"schedule.json") as file:
			GoogleDriveManager.text = file.read();
		#^^automatically close the file 
	else:
		if DELETE_USED:
			os.system('rm -rf data/*');
		GoogleDriveManager.getSchedule();
	Reminder.parse(GoogleDriveManager.text);
	with open(currentFolder+"schedule.json", mode="w") as file:
		file.write(GoogleDriveManager.text);
	reminderLabel.configure(text="reminders ready!");
	global finishedLoading;
	finishedLoading = True;
class Main:
	lastReminder = None;
	lastTimeChecked = time.time();
	checkedNewReminder = True;
	@staticmethod
	def onInteract():
		Main.lastTimeChecked = time.time();
		BrightnessManager.setBrightness(100);
		if (not Main.checkedNewReminder):
			Main.checkedNewReminder = True;
			reminderLabel.configure(bg = "#b8faff");
	@staticmethod
	def repeat(): 
		print("repeats")
		if (Main.lastReminder != None):
			if (Main.lastReminder.audio != None):
				Speaker.play(Main.lastReminder.audio);
	@staticmethod
	def btn2(): #don't know what this btn do (yet)
		pass;
	@staticmethod
	def setup():
		# timeLabel.bind("<Button>", lambda e: Main.repeat());
		reminderLabel.bind("<Button>", lambda e: Main.repeat());
		repeatBtn.configure(command=Main.repeat);
		def onAnyPressed(e):
			print("yes");
			reminderLabel.configure(bg = "#b8faff");
			Main.repeat();
		root.bind("<Return>", onAnyPressed);
		root.after(100, loadReminders);
	@staticmethod
	def getReminder(currTime:str):
		global reminders;
		if (currTime in reminders.keys()):
			return reminders[currTime];
		else:
			return None;
	@staticmethod
	def update():
		"""insert documentation here"""
		# playsound("hitCow.mp3", True);
		global integer;
		localTime = time.localtime();
		currentTime = formatTime(localTime);
		currentReminder = Main.getReminder(currentTime);
		if (currentReminder != None):
			Main.lastReminder = currentReminder;
			currentReminder.show();
		# integer += 1;
		BrightnessManager.batterySave();
		timeLabel.configure(text=currentTime);
		print("tick");
		secTilNxtMin = 60 - localTime.tm_sec;
		root.after(secTilNxtMin*1000+10, Main.update);
		print("til next");
	# TimeLabel = ttk.Label(frm, text="a").grid(column=0, row=0)
	# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
Main.setup();
Main.update();
root.mainloop();
