import json;
from PIL import ImageTk, Image;
Global = None;
Main = None;
from src.controllers import Speaker, GoogleDriveManager;
def setup(_global, _Main):
	"""
	a subsitution for import method. This is used to avoid cyclic import statements \n
	imports the required classes
	"""
	global Global; Global = _global;
	global Main; Main = _Main;

	
class Reminder:
	"""stores the required resources and data for each reminder"""
	@staticmethod
	def parse(data:str):
			"""
	 		parse a dictionary of string into a dictionary of reminders\n
	 		@params: \n
			data:str the dictionary of string that will be parsed
	 		"""
			reminders = Global.reminders;
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
	isComplete = False;
	def new(data:dict):
		"""
		creates a new Reminder object using datas from the dictionary \n
	 		 will call **GoogleDriveManager.download** if the image/audio file is not downloaded yet\n
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
		Global.reminderLabel.configure(text= this.text, bg = "#8aff78");
		Main.checkedNewReminder = False;
		#TODO: add new reminder FX
		if (this.audio != None):
			print(this.audio);
			Speaker.play(this.audio);
		if (this.imgSrc != None):
			Global.imageLabel.configure(image = this.loadImage());
	def loadImage(this):
		"""loads the reminder image using the file path stored in the instance variable **imgSrc** and adjust the size to *(60px x 60px)* """
		if this.img != None:
			return this.img;
		this.img = ImageTk.PhotoImage(Image.open(this.imgSrc).resize((60, 60)));
		return this.img;
	def endTask(this):
		"""if this task is not marked as complete, use GoogleDriveManager to tell the server that the user did not complete this task on time. The user missed the task."""
		#handle code when reminder ends:
		if this.isComplete: 
			return;
		GoogleDriveManager.sendMissTask(this);
	def completeTask(this):
		"""mark this task/reminder as complete and use GoogleDriveManager to contact the server to notify user's family members"""
		this.isComplete = True;
		GoogleDriveManager.sendFinishTask(this);
#TODO: setup raspberry pi speaker
