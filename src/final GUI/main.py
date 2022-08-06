###### Import Statements #######
from tkinter import *;         # for GUI
import time;import os;         #  
from PIL import ImageTk, Image # regular tkinter image only supports .png										 
from pygame import mixer;      # is .wav better for pygame than mp3?
################################
#from playsound import playsound;
import src.controllers;
import src.sprites;
from src.sprites import SpriteBtn;
import src.Reminder;
Reminder = src.Reminder.Reminder;
from src.controllers import Speaker,BrightnessManager,GoogleDriveManager, Color;
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
	print('a')
	# return;
	currentFolder = f'./data/{Global.month}-{Global.date}/';
	if Global.NOLOAD_WHEN_EXIST and os.path.exists(currentFolder):
		print('already loaded :D');
		with open(currentFolder+"schedule.json") as file:
			GoogleDriveManager.text = file.read();
		#^^automatically close the file 
	else:
		if Global.DELETE_USED:
			os.system('rm -rf data/*');
		GoogleDriveManager.getSchedule();
		print(GoogleDriveManager.text=="");
		return;
	# Reminder.parse(GoogleDriveManager.text);
	with open(currentFolder+"schedule.json", mode="w") as file:
		file.write(GoogleDriveManager.text);
	Global.reminderLabel.configure(text="reminders ready!");
	global finishedLoading;
	finishedLoading = True;
	# Global.root.after(5000,Main.transToBlack);


class Global:
	DELETE_USED = True;
	HAVE_DISPLAY = False;
	CAN_QUIT_APP = True;
	NOLOAD_WHEN_EXIST = True;
	FPS = int(1000/30); #30 FPS
	########## initialize app and variables ###############################
	mixer.init();                                                         # initialize music player
	TIME_REMINDER_FONT = ("Oswald", 20, "bold");                          # set up fonts
	REMINDER_FONT = ("Oswald", 15, "normal");                             #
	root = Tk();                                                          #
	#root.wm_attributes('-fullscreen', 'True');                            # 
	screenW:int = 200;                                                    # 
	screenH:int = 300;                                                    #
	frm = Frame(root);                                                    # set up window
	root.configure(highlightthickness=0,background='#219ebc');            #
	frm.grid();                                                           #
	root.geometry(str(screenW)+"x"+str(screenH));                         #
	timeLabel = Label(frm, text="Loading Time...", font = TIME_REMINDER_FONT);       # Label that shows time
	timeLabel.configure(bg='#219ebc', foreground = "white");              #
	timeLabel.pack();                                                     #
	#######################################################################
	#################  Reminder Label  #######################################################
	reminderLabel = Label(root, text="Loading Data...");                                                #
	photo =  ImageTk.PhotoImage(Image.open("src/icon.jpg").resize((60, 60)));#TODO: change this to                            #
	# photo = photo.subsample(int(photo.width() / 60+0.5));                                  #
	reminderLabel.place(x=screenW/2-80,y=screenH/2-60);                             				 #
	reminderLabel.configure(bg='#219ebc', foreground = "white", font = REMINDER_FONT);       #																									 #
	################  Image Label  ###########################################################
	imageLabel = Label(root, text="hi",image = photo);																	 		 #
	imageLabel.place(x=screenW/2+10,y=screenH/2-20);																				 #
	imageLabel.configure(bg='#219ebc', foreground = "white");																 #
	##########################################################################################
	@staticmethod
	def exitApp():
		Global.root.destroy();
	exitButton = Button(root,text ='exit app', command = exitApp);
	exitButton.place(x=screenW/2-80,y=screenH/2);																				 #
	exitButton.configure(bg='#219ebc', foreground = "white");
	repeatBtnImg = ImageTk.PhotoImage(Image.open("src/repeat-normal.png").resize((int(95/1.5),int(60/1.5))));
	# repeatBtn = Label(root,text ='Repeat',image=repeatBtnImg); #configed in Main.setup
	repeatBtn = SpriteBtn(x=screenW/2-80,y=screenH/2+40, name="repeat");
	# repeatBtn.place(x=screenW/2-80,y=screenH/2+40);																				 #
	repeatBtn.object.configure(bg='#219ebc', foreground = "white", font = REMINDER_FONT);
	
	reminders = {"":""};
	month = time.localtime().tm_mon;
	date = time.localtime().tm_mday;
	currentPage = "Main";



class Main:
	completeButton = None;
	lastReminder = None;
	lastTimeChecked = time.time();
	checkedNewReminder = True;
	
	@staticmethod
	def onInteract():
		Main.lastTimeChecked = time.time();
		BrightnessManager.setBrightness(100);
		if (not Main.checkedNewReminder):
			Main.checkedNewReminder = True;
			Global.reminderLabel.configure(bg = "#219ebc");
	@staticmethod
	def repeat(this=None): 
		print("repeats")
		if (Main.lastReminder != None):
			if (Main.lastReminder.audio != None):
				Speaker.play(Main.lastReminder.audio);
	@staticmethod
	def btn2(): #don't know what this btn do (yet)
		pass;
	repeatBtnHover = ImageTk.PhotoImage(Image.open("src/repeat-hover.png").resize((int(95/1.5),int(60/1.5))));
	raff = ImageTk.PhotoImage(Image.open("src/repeat-clicked.png"));
	@staticmethod
	def setup():
		Main.completeButton = SpriteBtn(x=Global.screenW/2+20,y=Global.screenH/2+40,name="complete",animationSize=9);
		Main.completeButton.object.configure(bg='#219ebc', foreground = "white");
		def completeTask(this):
			this.disableButton();
			print('button disabled');
			Color.transTo(Color.GREEN_THEME);			
			if Main.lastReminder != None:	
				Main.lastReminder.completeTask();
			else:
				print('no reminders are assigned');
		Main.completeButton.func = completeTask;
		# timeLabel.bind("<Button>", lambda e: Main.repeat());
		Global.reminderLabel.bind("<Button>", lambda e: Main.repeat());
		# Global.repeatBtn.bind("<ButtonRelease>",lambda e: print('yes'));
		# Global.repeatBtn.bind("<ButtonPress>",lambda e: Global.repeatBtn.configure(image=Main.repeatBtnHover));
		# Global.repeatBtn.bind("<Leave><ButtonRelease>",lambda e: Global.repeatBtn.configure(image=Global.repeatBtnImg));
		Global.repeatBtn.func = Main.repeat;
		Global.root.after(120, loadReminders);
	@staticmethod
	def getReminder(currTime:str):
		if (currTime in Global.reminders.keys()):
			return Global.reminders[currTime];
		else:
			return None;
	x = 0;
	spdX = 0;
	@staticmethod
	def update():
		"""insert documentation here"""
		# playsound("hitCow.mp3", True);
		global integer;
		localTime = time.localtime();
		currentTime = formatTime(localTime);
		currentReminder = Main.getReminder(currentTime);
		if (currentReminder != None):
			if Main.lastReminder != None:
				Main.lastReminder.endTask();
			Main.lastReminder = currentReminder;
			currentReminder.show();
			Main.completeButton.enableButton();
		# integer += 1;
		BrightnessManager.batterySave();
		Global.timeLabel.configure(text=currentTime);
		print("tick");
		Main.x += Main.spdX;
		Main.spdX += 1;
		if Main.x > 40:
			Main.spdX -=2;
		secTilNxtMin = 60 - localTime.tm_sec;
		Global.root.after(secTilNxtMin*1000+10, Main.update);
		print("til next");
		def p():
			print('a')
		# Global.root.after(int(1000/60), Main.update); #set frame rate to 60 FPS, run every frame
		#root.after(1,Main.update); # run every frame without limit
	# TimeLabel = ttk.Label(frm, text="a").grid(column=0, row=0)
	# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)

#==========




Sprite = src.sprites.Sprite;
src.sprites.setup(Global);


src.controllers.setup(Global,Main,Sprite);

src.Reminder.setup(Global,Main);
Main.setup();

import src.settings;
src.settings.setup(Global,Main);
Main.update();
Global.root.mainloop();
#TODO: post processing
#TODO: settings
#TODO: battery show
