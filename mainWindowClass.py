"""		  Projet Arduino		"""
"""		fenetre principale		"""

from tkinter import Tk, Frame, BOTH

class mainWindow(Frame):

	def __init__(self, parent):
		Frame.__init__(self, parent, background="white")

		self.parent = parent

		self.initUI()

	def initUI(self):

		self.parent.title("Simple")
		self.pack(fill=BOTH, expand=1)
		self.centerWindow()

	def centerWindow(self):
		w = 600
		h = 400

		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()

		x = (sw - w)/2
		y = (sh - h)/2
		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
