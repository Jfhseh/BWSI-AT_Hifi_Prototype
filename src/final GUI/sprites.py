from PIL import ImageTk, Image; 
from tkinter import Label;
from src.controllers import Speaker;
screenW =None; screenH=None;  root=None;  FPS = None;
def setup(_global): #get global vars
	"""
	a subsitution for import method. This is used to avoid cyclic import statements \n
	imports the required classes
	"""
	global screenW, screenH, root, FPS;
	screenW =_global.screenW; screenH = _global.screenH;
	root = _global.root; FPS = _global.FPS;
	

class Sprite:
	"""
 	adds animation to the tkinter widgets\n
	**composition** - the Sprite *has a* tkinter widget, but it's not inheritance
 	"""
	#static vars
	sprites = [];
	#
	object = None;
	x = 0;
	spdX = 0;
	y = 0;
	origX = 0; origY = 0;
	isHidden = False;
	def __init__(this, object,x,y):
		"""
		inits the sprite with the target tkinter widget \n
		Parameters
		--------------------
		object - the original tkinter widget\n
		x:float - the x position of the sprite\n
		y:float - the y position of the sprite
		"""
		Sprite.sprites.append(this);
		this.object = object;
		this.origX = this.x = x;
		this.origY = this.y = y;
		this.size = 100;
		this.update();
	def slideRight(this):
		"""
		starts an animation that slides this sprite into the GUI \n
		calls **this.update** each frame for animation
		"""
		#TODO
		this.spdX = 0;
		def slide():
			this.spdX += 4;
			this.x += this.spdX;
			this.update();
			print('tick')
			if (this.x-this.origX < screenW):
				root.after(FPS, slide);
		slide();
	def slideLeft(this):
		"""
		starts an animation that slides this sprite out of the GUI \n
		calls **this.update** each frame for animation
		"""
		#TODO
		this.spdX = 0;
		def slide():
			this.spdX -= 4;
			this.x += this.spdX;
			this.update();
			print('tick')
			if (this.x > this.origX):
				root.after(FPS, slide);
			else: 
				this.x = this.origX;
				this.y = this.origY;
				this.update();
		slide();
	def update(this):
		"""
		updates this sprite's position on the screen
		"""
		if not this.isHidden:
			print(f"({this.x},{this.y})");
			this.object.place(x=this.x,y=this.y);
	def hide(this):
		"""
		hide this sprite from the GUI
		"""
		this.isHidden = True;
		this.object.place_forget();
	def show(this):
		"""
		show this sprite on the GUI
		"""
		this.isHidden = False;
		this.update();

class SpriteBtn(Sprite):
	"""
 	**inheritance** - this class *is a* Sprite with button function \n
	used to create buttons using images and animations instead of ordinary tkinter buttons.
 	"""
	status = "normal";
	image = None;
	normalSrc = None;
	hoverSrc = None;
	clickedSrc = None;
	func = lambda _,this: print('no button function');
	def __init__(this,x,y, name, animationSize = 0):
		"""
		creates the ButtonSprite with the name of this sprite for loading images \n
		and the size of the animation(if there is one) \n
		runs this.func(needs to be overrided) when the button is activated.\n
		the default this.func prints "no button function" \n
		Parameters
		--------------
		x:float the x position of this sprite\n
		y:float the y position of this sprite\n
		name:str the name of this sprite (for loading images & animations)\n
		animationSize:int the length of the animation (if there is one) \n\n
		The press-and-hold button is activated by pressing and holding on the button \n
		the action will be canceled if the user releases the button before the hold animation stop once the user moves the finger out of the button
		"""
		object = Label(root);
		super().__init__(object,x,y);
		if animationSize == 0:
			this.object.bind("<ButtonPress>", lambda e: this.onSelect());
			this.object.bind("<Leave>", lambda e: this.onUnselect());
			this.object.bind("<ButtonRelease>", lambda e: this.onClicked());
			this.normalSrc = this.loadImage(f"src/{name}-normal.png");
			this.hoverSrc = this.loadImage(f"src/{name}-hover.png");
			this.clickedSrc = this.loadImage(f"src/{name}-clicked.png");
		else:
			this.object.bind("<ButtonPress>", lambda e: this.onSelect());
			this.object.bind("<Leave>", lambda e: this.onUnselect());
			this.object.bind("<ButtonRelease>", lambda e: this.onUnselect());
			#button function is called by pressing and holding
			this.normalSrc = this.loadImage(f"src/{name}/{name}-normal.png");
			this.hoverSrc = [];
			for i in range(animationSize):
			 this.hoverSrc.append(this.loadImage(f"src/{name}/{name}-hover{i+1}.png"));
			this.clickedSrc = this.loadImage(f"src/{name}/{name}-clicked.png");
		this.update();
			
	def update(this):
		"""
		calls **super.updates** to update this sprite's position on the screen\n
		updates the animation of this sprite by loading a new image to the tkinter label
		"""
		super().update();
		status = this.status;
		if status == "normal":
			this.image = this.normalSrc;
		elif status == "selected":
			if type(this.hoverSrc) != list:
				#no animation
				this.image = this.hoverSrc;
				print('hia')
		elif status == "clicked":
			this.image = this.clickedSrc;
		elif status == "disabled":
			this.image = this.hoverSrc[0];
		this.object.configure(image = this.image);
	def onSelect(this):
		"""
		this method is called when the button is selected (pressed but not released) \n
		this does not run if the button is disabled \n
		plays a select sound and updates the screen \n
		if this button is a press-and-hold button, then starts the hold animation
		"""
		print(this.status)
		if this.status == "disabled":
			print('disabled')
			return;
		Speaker.playSound("src/hover.wav");
		this.status = "selected";
		this.update();
		if type(this.hoverSrc) == list: #animate
			animationSize = len(this.hoverSrc);
			def animate(i):
				print(f"animation: playing animation: {i}")
				if this.status != "selected":
					print('animation: canceled')
					return;
				this.image = this.hoverSrc[i];
				this.update();
				if i+1 < animationSize:
					root.after(FPS*3,lambda:animate(i+1));
				else: 
					print('animation: done')
					Speaker.playSound("src/complete.wav");
					root.after(FPS*2,lambda:this.onClicked());
			animate(0);
	def onUnselect(this):
		"""
		this method is run when the user unselect the button \n
		does not run when the button is disabled \n
		updates the screen when this method is called
		"""
		if this.status == "disabled":
			return;
		this.status = "normal";
		this.update();
	def onClicked(this):
		"""
		runs **this.func** when the button is clicked \n
		note: this.func needs to be set by other code to give this button a function.
		does not run when the button is disabled \n
		updates the screen when this method is called
		"""
		if this.status == "disabled":
			return;
		if this.status == "normal":
			return;
		this.status = "clicked";
		this.update();
		this.func(this);
		def noClick():
			if this.status == "clicked":
				this.onUnselect();
		root.after(FPS, noClick);
	#to be used in func
	def disableButton(this):
		"""
		disables this button, and the button will not listen to any select,unselect, or click/activate event until it is re-enabled.
		"""
		this.status = "disabled";
		this.update();
		print('button disabled');
	def enableButton(this):
		"""
		enables the button so it will listen to select,unselect, and click/activate events.
		"""
		this.status = "normal";
		print('button enabled');
		this.update();
	def resize(this, src, size):
		"""
		resize a image to a appropriate size provided by the parameters \n
		Parameters
		---------------
		src:str the file path to the image\n
		size: the desired size of the image
		"""
		return ImageTk.PhotoImage(Image.open(src).resize((int(95/1.5*size),int(60/1.5*size))));
	def loadImage(this, src):
		"""
		loads a image for this button \n
		Parameters
		---------------
		src:str the file path to the image
		"""
		return ImageTk.PhotoImage(Image.open(src).resize((int(95/1.5),int(60/1.5))));
