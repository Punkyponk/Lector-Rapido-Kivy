from kivy.uix.label import Label
from kivy.properties import ListProperty
from kivy.graphics import Color, Rectangle

class ColorLabel(Label):
	background_color = ListProperty([0.75,0.75,0.75,1])
	def actualizarColor(self):
		self.canvas.before.clear()
		with self.canvas.before:
			VR,VG,VB,VA = self.background_color
			Color(VR,VG,VB,VA)
			Rectangle(pos=self.pos, size=self.size)
	def on_size(self, *args):
		self.actualizarColor()
	def on_background_color(self, instance, ps):
		self.actualizarColor()
