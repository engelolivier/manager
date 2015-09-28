#!/usr/bin/env python3
# coding: utf-8

from gi.repository import Gtk
import sys

class Interface:
	__gtype_name__ = "Interface"

	def __init__(self):

		self.builder = Gtk.Builder()
		self.builder.add_from_file("interface.glade")
		
		self.window = self.builder.get_object("window1")
		self.window.show_all()

		dic = {
			"on_buttonQuit_clicked" : self.quit,
			# "on_button1_clicked" : self.on_button1_clicked,
			"on_window1_destroy": self.quit,
			# "entry1_key_press_event_cb" : self.entry1_key_press_event_cb
		}

		self.builder.connect_signals(dic)

	"""

	def on_button1_clicked(self, widget):

		entry1 = self.builder.get_object("entry1")
		entry1.get_text()
		print(entry1.get_text())

		import requests

		data               = {}
		data['name']       = entry1.get_text()
		data['date_start'] = "2015-01-01 00:00:00"
		data['date_end']   = "2015-01-03 00:00:00"

		headers = {'Authorization': 'Token 9b9209a011e16a94a61e36688d4d29d8bb580544'}
		r = requests.post('http://localhost:8000/api/task/', headers=headers, data=data)

	def entry1_key_press_event_cb(self, widget):

		self.on_button1_clicked(widget)

	"""

	def quit(self, widget):
		print("Exit...")
		sys.exit(0)

if __name__ == '__main__':
	Interface()
	Gtk.main()
