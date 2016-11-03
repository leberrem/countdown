import time
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

import RPi.GPIO as GPIO

beepPin = 17
defaultTime = 900 # 15 minutes
colorTime = 120 # 2 minutes
interval = 1 # 1 seconde

GPIO.setmode(GPIO.BCM)
GPIO.setup(beepPin, GPIO.OUT)
GPIO.output(beepPin, GPIO.LOW)

class TimerApp(App):

	temps = defaultTime
	label = None
	startButton = None
	initButton = None
	lessButton = None
	moreButton = None
	alive = 0
	event = None

	def buzzer_off(self):
		#print ("buzzer off")
		GPIO.output(beepPin, GPIO.LOW)

	def buzzer_on(self):
		#print ("buzzer on")
		GPIO.output(beepPin, GPIO.HIGH)

	def click(self):
		self.buzzer_on();
		time.sleep(.1)
		self.buzzer_off();

	def endBuzz(self):
		self.buzzer_on();
		time.sleep(.5)
		self.buzzer_off();
		time.sleep(.2)
		self.buzzer_on();
		time.sleep(.5)
		self.buzzer_off();
		
	def start_callback(self, obj):
		Clock.schedule_once(lambda dt: self.click(), 0)
		if (self.temps <= 0):
			self.temps = defaultTime;
		if (self.alive):
			self.event.cancel()
			obj.text = "START"
			self.initButton.disabled=False
			self.moreButton.disabled=False
			self.lessButton.disabled=False
			self.alive = 0
		else:
			obj.text = "STOP"
			self.initButton.disabled=True
			self.moreButton.disabled=True
			self.lessButton.disabled=True
			self.alive = 1
			self.event = Clock.schedule_interval(lambda dt: self.update(self.label), interval)

	def init_callback(self, obj):
		Clock.schedule_once(lambda dt: self.click(), 0)
		self.startButton.disabled=False
		self.moreButton.disabled=False
		self.lessButton.disabled=False		
		self.temps = defaultTime
		self.set_label()

	def more_callback(self, obj):
		Clock.schedule_once(lambda dt: self.click(), 0)
		self.temps += 60
		self.set_label()

	def less_callback(self, obj):
		Clock.schedule_once(lambda dt: self.click(), 0)
		if (self.temps - 60 > 0):
			self.temps -= 60
		self.set_label()

	def set_label(self):

		minutes = self.temps / 60
		secondes = self.temps % 60

		if (self.temps <= colorTime):
			self.label.text = "[color=ff3333]" + str(minutes).zfill(2) + ":" + str(secondes).zfill(2) + "[/color]"
		else:
			self.label.text = str(minutes).zfill(2) + ":" + str(secondes).zfill(2)

	def update(self, label):
		self.temps -= 1

		if (self.temps <= 0):
			self.event.cancel()
			self.startButton.text = "START"
			self.set_label()
			self.alive = 0
			self.initButton.disabled=False
			self.startButton.disabled=True
			Clock.schedule_once(lambda dt: self.endBuzz(), 0)
		else:
			self.startButton.disabled=False
			self.set_label()

		# print("temps = " + str(self.temps))


	def build(self):

		# Set up the layouts:
		layout1 = GridLayout(cols=1, rows=2, spacing=00, padding=0)
		layout2 = GridLayout(cols=4, rows=1, spacing=20, padding=20)

		# Set background:
		with layout1.canvas.before:
			#Color(.2,.2,.2,1)
			self.rect = Rectangle(size=(800,480), pos=layout1.pos, source='back.jpg')

		self.label = Label(font_size=200, markup=True)
		self.set_label()

		self.startButton = Button(text="START", font_size=30, background_color=(1, 1, 1, .6))
		self.startButton.bind(on_press=self.start_callback)

		self.initButton = Button(text="INIT", font_size=30, background_color=(1, 1, 1, .6))
		self.initButton.bind(on_press=self.init_callback)

		self.lessButton = Button(text="-", font_size=30, background_color=(1, 1, 1, .6))
		self.lessButton.bind(on_press=self.less_callback)

		self.moreButton = Button(text="+", font_size=30, background_color=(1, 1, 1, .6))
		self.moreButton.bind(on_press=self.more_callback)

		layout1.add_widget(self.label)
		layout1.add_widget(layout2)
		layout2.add_widget(self.startButton)
		layout2.add_widget(self.moreButton)
		layout2.add_widget(self.lessButton)
		layout2.add_widget(self.initButton)

		return layout1

TimerApp().run()
