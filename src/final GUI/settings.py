from tkinter import Scale, Button, Label, HORIZONTAL;
from src.sprites import Sprite, SpriteBtn;
from src.controllers import Speaker, Color;
Global = None;
reminderLABEL =None;
imgLabel = None;
btnLABEL = None;
def onPageChange(e):
	"""
 	runs when the user presses the setting button. \n
	switch the GUI from reminder page to setting page, or vice versa. \n
 	This starts all of current page's widgets's animation
 	"""
	print("yes");
	global hid;
	if not hid:
		btnLABEL.slideRight();
		imgLabel.slideRight();
		reminderLABEL.slideRight();
		Settings.slideRight();
		Main.completeButton.slideRight();
		Global.repeatBtn.slideRight();
		hid = True;
	else:
		btnLABEL.slideLeft();
		reminderLABEL.slideLeft();
		imgLabel.slideLeft();
		Settings.slideLeft();
		Main.completeButton.slideLeft();
		Global.repeatBtn.slideLeft();
		hid = False;
	Main.repeat();
def setup(_global,_Main):
		"""
		a subsitution for import method. This is used to avoid cyclic import statements \n
		imports the required classes
		"""
		global Global, Main; Global = _global; Main = _Main;
		global reminderLABEL,imgLabel,btnLABEL;
		reminderLABEL = Sprite(Global.reminderLabel,x=Global.screenW/2-90,y=Global.screenH/3-40);
		imgLabel =  Sprite(Global.imageLabel,x=Global.screenW/2+10,y=Global.screenH/2-40);
		btnLABEL = Global.repeatBtn;
		Global = _global;
		Main = Main;
		Settings.setup();
		Global.root.bind("<Return>", onPageChange);
hid = False;
class Settings:
	"""
 	all the code for widgets, GUI are stored here.
 	"""
	settingLABEL = None;
	volumeSlider = None;
	settingBtn = None;
	themeBtn = None;
	@staticmethod
	def onClick(this):
		"""
		 	runs when the user presses the setting button. \n
			switch the GUI from reminder page to setting page, or vice versa.
		"""
		currentPage = Global.currentPage;
		if (currentPage == "Settings"):
			currentPage = "Main";
		else:
			currentPage = "Settings";
		onPageChange(0);
	@staticmethod
	def setup():
		"""
		sets up the widgets in the setting oage
		"""
		Settings.volumeSlider = Sprite(Scale(Global.root, from_=0, to=100, orient=HORIZONTAL),20-Global.screenW,90);
		Settings.volumeSlider.object.configure(bg='#219ebc', foreground = "white", font = Global.REMINDER_FONT, command=Speaker.setVolume);
		Settings.settingBtn = SpriteBtn(x=50,y=Global.screenH-50, name="settings");
		Settings.settingBtn.object.configure(bg='#219ebc', foreground = "white", font = Global.REMINDER_FONT);
		Settings.settingBtn.func = Settings.onClick;
		Settings.settingLABEL = Sprite(Label(Global.root, text="settings: \n volume"),0-Global.screenW, 30);
		Settings.settingLABEL.object.configure(bg='#219ebc', foreground = "white", font = Global.REMINDER_FONT);
		Settings.themeBtn = SpriteBtn(x=0-Global.screenW,y=190,name="switchTheme");
		Settings.themeBtn.func =  lambda this:Global.root.after(1000,lambda:Color.transTo(Color.DARK_THEME) if Color.currentColor == Color.DEFAULT_THEME else Color.transTo(Color.DEFAULT_THEME));
		Settings.themeBtn.object.configure(bg='#219ebc', foreground = "white");
	def slideRight():
		"""
		make widgets from the settings to slide into the screen
		"""
		Settings.settingLABEL.slideRight();
		Settings.volumeSlider.slideRight();
		Settings.themeBtn.slideRight();
	def slideLeft():
		"""
		make widgets from the settings to slide out of the screen
		"""
		Settings.themeBtn.slideLeft();
		Settings.settingLABEL.slideLeft();
		Settings.volumeSlider.slideLeft();

	
