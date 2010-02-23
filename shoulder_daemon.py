import os
import gtk
import gobject

import dbus
import dbus.service
import dbus.mainloop.glib
import pynotify

class ShoulderLauncher(dbus.service.Object):

    @dbus.service.method("com.cued.ShoulderLauncher", in_signature='s', out_signature='s')
    def LaunchApp(self, launch_cmd):
      print "launching command " + str(launch_cmd)
      n = pynotify.Notification("Launching " + str(launch_cmd), "on the local machine")
      n.show()
      return "success"

class TrackerStatusIcon(gtk.StatusIcon):
	def __init__(self):
		gtk.StatusIcon.__init__(self)
		menu = '''
			<ui>
			 <menubar name="Menubar">
			  <menu action="Menu">
			   <menuitem action="Sleep Desktop"/>
			   <menuitem action="Exit"/>
			   <separator/>
			   <menuitem action="About"/>
			  </menu>
			 </menubar>
			</ui>
		'''
		actions = [
			('Menu',  None, 'Menu'),
			('Sleep Desktop', None, '_Sleep Deskop...', None, 'Forces the desktop to sleep', self.sleep_desktop),
			('Exit', gtk.STOCK_QUIT, '_Exit', None, 'Exit the daemon', self.on_exit),
			('About', gtk.STOCK_ABOUT, '_About...', None, 'About Shoulder', self.on_about)]
		ag = gtk.ActionGroup('Actions')
		ag.add_actions(actions)
		self.manager = gtk.UIManager()
		self.manager.insert_action_group(ag, 0)
		self.manager.add_ui_from_string(menu)
		self.menu = self.manager.get_widget('/Menubar/Menu/About').props.parent
		search = self.manager.get_widget('/Menubar/Menu/Search')
		self.set_from_stock(gtk.STOCK_FIND)
		self.set_tooltip('Tracker Desktop Search')
		self.set_visible(True)
		self.connect('activate', self.on_activate)
		self.connect('popup-menu', self.on_popup_menu)

	def on_activate(self, data):
		self.menu.popup(None, None, None, 1, 0)
	
	def sleep_desktop(self):
		print 'sleeping desktop'
		
	def on_popup_menu(self, status, button, time):
		self.menu.popup(None, None, None, button, time)

	def on_exit(self, data):
		gtk.main_quit()

	def on_about(self, data):
		dialog = gtk.AboutDialog()
		dialog.set_name('Shoulder')
		dialog.set_version('0.1.0')
		dialog.set_comments('The shoulder binds the ARM to the torso')
		dialog.set_website('jmaustin.org')
		dialog.run()
		dialog.destroy()

if __name__ == '__main__':

	TrackerStatusIcon()
	
	from dbus.mainloop.glib import DBusGMainLoop
	DBusGMainLoop(set_as_default=True)
	pynotify.init("Shoulder Launcher")
 	session_bus = dbus.SessionBus()
   	name = dbus.service.BusName("com.cued.Shoulder", session_bus)
	object = ShoulderLauncher(session_bus, '/ShoulderLauncher')
	gtk.main()

