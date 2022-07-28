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
#root.wm_attributes('-fullscreen', 'True');                            # 
screenW:int = 200;                                                    # 
screenH:int = 200;                                                    #
frm = Frame(root);                                                    # set up window
root.configure(highlightthickness=0,background='#b8faff');            #
frm.grid();                                                           #
root.geometry(str(screenW)+"x"+str(screenH));                         #
timeLabel = Label(frm, text="Loading Time...", font = TIME_REMINDER_FONT);       # Label that shows time
timeLabel.configure(bg='#b8faff', foreground = "black");              #
timeLabel.pack();                                                     #
#######################################################################
#################  Reminder Label  #######################################################
reminderLabel = Label(root, text="Loading Data...");                                                #
photo =  ImageTk.PhotoImage(Image.open("000.png").resize((60, 60)));#TODO: change this to                            #
# photo = photo.subsample(int(photo.width() / 60+0.5));                                    #
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
exitButton.place(x=screenW/2-80,y=screenH/2);																				 #
exitButton.configure(bg='#b8faff', foreground = "black");
repeatBtn = Button(root,text ='Repeat'); #configed in Main.setup
repeatBtn.place(x=screenW/2-80,y=screenH/2+40);																				 #
repeatBtn.configure(bg='#b8faff', foreground = "black");
reminders = {"":""};
month = time.localtime().tm_mon;
date = time.localtime().tm_mday;
class BrightnessManager:
	"""controls the brightness of the display"""
	@staticmethod
	def setBrightness(percent):
		"""set brightness of the display;
			does not run when **HAVE_DISPLAY** == False"""
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
	"""download files from google drive and communicates with the Appscript server"""
	text = "";
	@staticmethod
	def getSchedule():
		"""
		send a get request to Appscript server;
		stores the respond from the server to **GoogleDriveManager.text**
		"""
		print("GoogleDriveManager: getting schedule");
		currentFolder = f'./data/{month}-{date}/';
		#vv need to be changed if appscript version changed
		x = requests.get('https://script.google.com/macros/s/AKfycbwKfXO-Z4knGNjHHP0FeXnzb30RQinub5WTka9OKmpAB3sZC0AVVzwd8MnGoENjetp7oQ/exec');
		print(x.status_code);
		print(x.text);
		#^^automatically close the file 
		GoogleDriveManager.text = x.text;
	@staticmethod
	def download(fileID, fileExtension, time):
		"""
		download a file from google drive \n
		@params: \n
		fileID:str - the fileID provided by the server 
		fileExtension:str - the file format that the downloaded file will be stored into (.png, .wav...) \n
		time:str the time that this file will be used (also provided by the server)
		"""
		file = str(month)+"-"+str(date)+"-"+time+fileExtension;
		dest = f"./data/{month}-{date}/{file}";
		gdd.download_file_from_google_drive(fileID, dest);
		return dest[2:];
class Reminder:
	"""stores the required resources and data for each reminder"""
	@staticmethod
	def parse(data:str):
			"""
	 		parse a dictionary of string into a dictionary of reminders
	 		@params: \n
			data:str the dictionary of string that will be parsed
	 		"""
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
		"""
		creates a new Reminder object using datas from the dictionary \n
	 		 will call **GoogleDriveManager.download** if the image/audio file is not downloaded yet
			@params: \n
			data:dict the required datas for the Reminder object
		"""
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
		"""
	 	shows this reminder using the **reminderLabel** and **imagelabel* \n
		calls **Speaker.play** for audio reminder \n
	 	image is automatically adjusted to size *(60px x 60px)*
	 	"""
		reminderLabel.configure(text= this.text, bg = "#8aff78");
		Main.checkedNewReminder = False;
		#TODO: add new reminder FX
		if (this.audio != None):
			print(this.audio);
			Speaker.play(this.audio);
		if (this.imgSrc != None):
			imageLabel.configure(image = this.loadImage());
	def loadImage(this):
		"""loads the reminder image using the file path stored in the instance variable **imgSrc** and adjust the size to *(60px x 60px)* """
		if this.img != None:
			return this.img;
		this.img = ImageTk.PhotoImage(Image.open(this.imgSrc).resize((60, 60)));
		return this.img;
#TODO: setup raspberry pi speaker
class Speaker:
	"""
 		controls the audio\n
		uses **pygame.mixer** for audio playing
 	"""
	@staticmethod 
	def setup():
		"""connect to the speaker if needed"""
		pass;
	
	@staticmethod
	def play(fileName:str):
		"""
		@note - a new reminder notification sound will be played before the audio file
		play a .mp3 or .wav using **pygame.mixer** \n
		@params: \n
		fileName:str the fileName of the audio file
		"""
		mixer.music.load("newReminder.wav");
		mixer.music.play(1);
		def after():
			"""plays the audio file after new reminder notification"""
			mixer.music.load(fileName);
			mixer.music.play(1);
		root.after(2001,after);
		# playsound(fileName,False);
		print("Playing audio");			

def formatTime(currentDateTime):
		"""
		format current time into the format hh:mm \n
		@params: \n
		currentDateTime:Time time.localtime() \n
		@returns:str the formatted time stored in a string
		"""
    hr = str(currentDateTime.tm_hour);
    min = str(currentDateTime.tm_min);
    if (len(hr) == 1):
        hr = "0"+hr;
    if (len(min) == 1):
        min = "0"+min;
    return hr+":"+min;
	
#TODO: delete return
def loadReminders():	
	"""
 	load today's reminders stored in the server \n
 	uses **GoogleDriveManager** for sending the get request to the server. \n \n
	- **if** today's reminders are already loaded, then open the already loaded *schedule* file and read the schedule \n \n
 	removes all files in the data folder before loading **if** the constant **NOLOAD_WHEN_EXIST** == True \n \n
	AFTER REMINDERS ARE LOADED: \n
	- the **finishedLoading** variable will be set to **True** \n
 	- "reminders ready!" will be shown in the reminderLabel
 	"""
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
	"""
 		 controls the "main loop" for the GUI \n
 		 update the **timeLabel** and reminderLabel** in the main loop
	"""
	lastReminder = None;
	lastTimeChecked = time.time();
	checkedNewReminder = True;
	@staticmethod
	def onInteract():
		"""
		Hide the text highlight when the user interacts with the device \n
		- updates static variable **lastTimeChecked**
		- updates screen brightness using the **BrightnessManager**
		"""
		Main.lastTimeChecked = time.time();
		BrightnessManager.setBrightness(100);
		if (not Main.checkedNewReminder):
			Main.checkedNewReminder = True;
			reminderLabel.configure(bg = "#b8faff");
	@staticmethod
	def repeat(): 
		"""
		repeats the reminder when the "repeat" button is pressed \n
		plays the audio reminder again using **Speaker.play** \n
		- does not do anything if **Main.lastReminder** doesn't have audio file or doesn't exist
		"""
		print("repeats")
		if (Main.lastReminder != None):
			if (Main.lastReminder.audio != None):
				Speaker.play(Main.lastReminder.audio);
	@staticmethod
	def btn2(): #don't know what this btn do (yet)
		pass;
	@staticmethod
	def setup():
		"""
		set up the labels, buttons, and load today's reminders using the **loadReminders** function
		"""
		# timeLabel.bind("<Button>", lambda e: Main.repeat());
		reminderLabel.bind("<Button>", lambda e: Main.repeat());
		repeatBtn.configure(command=Main.repeat);
		def onAnyPressed(e):
			print("yes");
			reminderLabel.configure(bg = "#b8faff");
			Main.repeat();
		root.bind("<Return>", onAnyPressed);
		root.after(120, loadReminders);
	@staticmethod
	def getReminder(currTime:str):
		"""
		get the current reminder from the dictionary **reminders** \n
		returns **None** if the reminder doesn't exist \n
		@params: \n
		currTime:str the current time formatted in hh:mm (by the **formatTime** function)
		"""
		global reminders;
		if (currTime in reminders.keys()):
			return reminders[currTime];
		else:
			return None;
	@staticmethod
	def update():
		"""
		the main loop for the GUI
		- updates the **timeLabel** and **reminderLabel** as intended \n
		- turn on batterySaving mode if the device is not used for 3 minutes using the **BrightnessManager.batterySave** \n
		- updates every minute
		"""
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
#TODO: repeat btn
#TODO: battery show
