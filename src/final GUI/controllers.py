import time;
import screen_brightness_control as sbc;
import requests;
from google_drive_downloader import GoogleDriveDownloader as gdd;
from pygame import mixer; 
Global = None;
Main = None;
Sprite = None;
def setup(_global,_Main, _Sprite):
		"""
		a subsitution for import method. This is used to avoid cyclic import statements \n
		imports the required classes
		"""
		global Global, Main,Sprite;
		Global = _global;
		Main = Main;
		Sprite = _Sprite;


class BrightnessManager:
	"""@deprecated, not used in the final product"""
	@staticmethod
	def setBrightness(percent):
		if not Global.HAVE_DISPLAY:
			return;
		sbc.set_brightness(percent);
	@staticmethod
	def batterySave():
		"""reset display brightless _**if**_ the device is left 3min idle"""
		if not Global.HAVE_DISPLAY:
			return;
		if (time.time() - Main.lastTimeChecked < 180):
			return;
		BrightnessManager.setBrightness(5);
class GoogleDriveManager:
	"""
 		download files from google drive and communicates with the Appscript server
 	"""
	text = "";
	@staticmethod
	def getSchedule():
		"""
		send a get request to Appscript server;\n
		stores the respond from the server to **GoogleDriveManager.text**
		"""
		print("GoogleDriveManager: getting schedule");
		# currentFolder = f'./data/{month}-{date}/';
		#vv need to be changed if appscript version changed
		x = requests.get('{insert webapp url here}');
		print(x.status_code);
		print(x.text);
		#^^automatically close the file 
		GoogleDriveManager.text = x.text;
	@staticmethod
	def download(fileID, fileExtension, time):
		"""
		download a file from google drive \n
		@params: \n
		fileID:str - the fileID provided by the server \n
		fileExtension:str - the file format that the downloaded file will be stored into (.png, .wav...) \n
		time:str the time that this file will be used (also provided by the server)
		"""
		file = str(Global.month)+"-"+str(Global.date)+"-"+time+fileExtension;
		dest = f"./data/{Global.month}-{Global.date}/{file}";
		gdd.download_file_from_google_drive(fileID, dest);
		return dest[2:];
	@staticmethod
	def sendFinishTask(task):
		"""
		sends a post request to the server, telling it which task did the user complete \n
		Parameters
		-----------------
		task:Reminder the task that the user just completed
		"""
		params = {
			"type":"completeTask",
			"taskName":task.text,
			"scheduleTime":task.time
		};
		x = requests.post('{insert webapp url here}',params=params);
		print(x.text);
		print(x.status_code);
	@staticmethod
	def sendMissTask(task):
		"""
		sends a post request to the server, telling it which task did the user miss \n
		Parameters
		-----------------
		task:Reminder the task that the user did not complete
		"""
		params = {
			"type":"missTask",
			"taskName":task.text,
			"scheduleTime":task.time
		};
		x = requests.post('{insert webapp url here}',params=params);
		print(x.text);
		print(x.status_code);
class Speaker:
	"""
 		controls the audio\n
		uses **pygame.mixer** for audio playing
 	"""
	@staticmethod 
	def setup():
		"""connect to the speaker if needed"""
		pass;
	def setVolume(v):
		"""
		@note - a new reminder notification sound will be played before the audio file\n
		play a .mp3 or .wav using **pygame.mixer** \n
		@params: \n
		fileName:str the fileName of the audio file
		"""
		mixer.music.set_volume(float(v)/100);
		print('volume to:'+v);
	@staticmethod
	def play(fileName:str):
		mixer.music.load("newReminder.wav");
		mixer.music.play(1);
		def after():
			"""plays the audio file after new reminder notification"""
			mixer.music.load(fileName);
			mixer.music.play(1);
		Global.root.after(2001,after);
		# playsound(fileName,False);
		print("Playing audio");			
	@staticmethod
	def playSound(fileName:str):
		"""
		plays an audio file without the newReminder notification sound \n
		(only use this when the audio file is not automatically played, such as a UI feedback SFX) \n
		Parameters
		--------------
		fileName:str the fileName of the audio file
		"""
		mixer.music.load(fileName);
		mixer.music.play(1);
		# playsound(fileName,False);
		print("Playing sound");			
class Color:
	"""
 	Controls the background color of the GUI\n
	all color-related methods and variables are stored in this class
 	"""
	DEFAULT_THEME = "#219ebc";
	DARK_THEME = "#121212";
	GREEN_THEME = "#4CBB17";
	currentColor = DEFAULT_THEME;
	@staticmethod
	def rgb_to_hex(rgb):
	"""
 	Converts RGB tuple to hexdecimal string for GUI usages \n
	Parameters
 	-----------------
	rgb:tuple the RGB value that is going to be converted \n

	Return
 	-----------------
	a hexdecimal string that represents the color
 	"""
		return '%02x%02x%02x' % rgb;
	@staticmethod
	def hex_to_rgb(value:str):
	"""
 	Converts hexdecimal string to RGB tuple for calculation usages \n
	Parameters
 	-----------------
	value:str	a hexdecimal string that represents the color \n
 
	Return
 	-----------------
	a tuple that represents the RGB value
 	"""
		value = value.lstrip('#')
		lv = len(value)
		return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))
	# (33, 158, 188)
	#(54,57,63)
	@staticmethod
	def transition(_from,_to, steps):
	"""
 	Parameters
	--------------
 	_from:str the hexdecimal string of the starting color \n
	_to:str the hexdecimal string of the target color that will be transitioned into \n
 	steps:int how fast the transition is (how many frames)\n
	
	Return
 	---------------
	an array of colors where the first item is the starting color and the last item is the target color \n
 	other items in the array are intermediate colors for smooth trnasition
 	"""
		_from = Color.hex_to_rgb(_from);
		_to = Color.hex_to_rgb(_to);
		ans = [];
		rStep = (_to[0]-_from[0]) / steps;
		gStep = (_to[1]-_from[1]) / steps;
		bStep = (_to[2]-_from[2]) / steps;
		for i in range(steps+1):
				rgb =(int(_from[0] + rStep*i), int(_from[1] + gStep*i), int(_from[2] + bStep*i));
				ans.append("#"+Color.rgb_to_hex(rgb));
		return ans;
	#color stuff
	@staticmethod
	def transTo(to):
		"""
		transition the background color into the desired color by using the **Color.transition** method \n
		Parameters
		---------------
		to:str the hexdecimal string that represents the desired color
		"""
		transitions = Color.transition(Color.DEFAULT_THEME,to,30);
		def transition(i):
			print('coloring'+str(i))
			Global.timeLabel.configure(bg=transitions[i]);
			Global.root.configure(bg=transitions[i]);
			for obj in Sprite.sprites:
				obj.object.configure(bg = transitions[i]);
				obj.object.update();
			if i+1 < len(transitions):
				Global.root.after(5*Global.FPS, transition(i+1));
			else:
				Color.currentColor = to;
		transition(0);
	
