#!/usr/bin/env python

import sys
import subprocess
import dbus, gobject
from dbus.mainloop.glib import DBusGMainLoop

APP_ID = "MediaKeys"
VERBOSE = (len(sys.argv) == 2) 

def runCmd(cmd):
	if VERBOSE:
		print "Running command: " + cmd
	try:
		ret = subprocess.call(cmd, shell=True)
	except subprocess.CalledProcessError:
		print "Failed to run " + cmdString
		pass
	except OSError:
		print "Could not find file to run"
		pass

	return ret;

def sendMusicControlCmd(action):
	cmd = "wget -q -O /dev/null http://localhost:8000/music?" + action
	return runCmd(cmd)

def sendiTunesCmd(action):
	cmd = "/home/mwettlaufer/scripts/iTunesControl.sh " + action
	return runCmd(cmd)

def mediakey_pressed(app, action):
   if app == APP_ID:
		if VERBOSE:
			print action + " key pressed."
		if sendiTunesCmd(action):
			if VERBOSE:
				print "Failed to run command"
			if sendMusicControlCmd(action):
				if VERBOSE:
					print "Failed to run command"
				print "Nowhere to send Media Keypress Event"
				print "Dropping on the floor"


def main():

	DBusGMainLoop(set_as_default=True)

	try:
		bus = dbus.SessionBus()
		mk = bus.get_object("org.gnome.SettingsDaemon","/org/gnome/SettingsDaemon/MediaKeys")
		mk.GrabMediaPlayerKeys(APP_ID, 0, dbus_interface='org.gnome.SettingsDaemon.MediaKeys')
		mk.connect_to_signal("MediaPlayerKeyPressed", mediakey_pressed)
		if VERBOSE:
			print "Bound media keys with DBUS"
	except dbus.DBusException:
		print "Failed to bind media keys with DBUS"
		exit(0)

	loop = gobject.MainLoop()
	loop.run()

if __name__ == "__main__":
	main()
