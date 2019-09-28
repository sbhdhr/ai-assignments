'''
Name : Subhashis Dhar
Roll No: 2019H1030023P
'''
from tkinter import *
class scrollTxtArea:
	def __init__(self,root):
		frame=Frame(root)
		frame.pack()
		self.textPad(frame)
		return

	def textPad(self,frame):
		#add a frame and put a text area into it
		textPad=Frame(frame)
		self.text=Text(textPad,width=70)
		
		# add a vertical scroll bar to the text area
		scroll=Scrollbar(textPad)
		self.text.configure(yscrollcommand=scroll.set)
		
		#pack everything
		self.text.pack(side=LEFT)
		scroll.pack(side=RIGHT,fill=Y)
		textPad.pack(side=TOP)
		return