# coding=utf-8
from __future__ import absolute_import
import sys


import octoprint.plugin
import urllib2 #Library to pull data from filaWeigher via http
import socket #Library to validate that the field is actually an IP address


class filaweigherPlugin(octoprint.plugin.SettingsPlugin,
						   octoprint.plugin.AssetPlugin,
						   octoprint.plugin.TemplatePlugin,
						   octoprint.plugin.StartupPlugin):

	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=True)
		]

#Set the default setting for the filaWeigher IP. Obviously, an IP will need to be
# set before it can work at all
	def get_settings_defaults(self):
		return dict(
			filaweigherIP="Enter FilaWeigher IP here",
		)

#Define the assets used for the front end. At the time of writing this comment
# I'm only using the .js
	def get_assets(self):
		return dict(
			js=["js/filaweigher.js"],
			css=["css/filaweigher.css"],
			less=["less/filaweigher.less"]
		)
#Start a timer to pull data from filaWeigher every X seconds. 
	def on_startup(self, host, port):
		self.t = octoprint.util.RepeatedTimer(10, self.check_sensors)
		self.t.start()

#Http request the data from filaWeigher
	def check_sensors(self):
		IPAddress = self._settings.get(["filaweigherIP"]) #grab IP from settings
		if self.is_valid_ipv4_address(IPAddress): #Check if it's a valid IP
			url = "http://" + IPAddress + "/json" #Create the URL string to use
			try: #Try connecting, and if it works, then send that data to the send_plugin_message
				# function. This function kicks off the .js function to parse the json from filaweigher
				# and update the frontend UI. 
				page = urllib2.urlopen(url)
				self._plugin_manager.send_plugin_message(self._identifier, page.read())
				#restart the timer. Because it may have been set to a higher internal
				# if it didn't connect, or cancelled completely if the the field didn't have
				# a valid IP address
				self.t.cancel()
				self.t = octoprint.util.RepeatedTimer(10, self.check_sensors)
				self.t.start()
			except:
				#If it couldn't connect, then set the timer to check again every 120 second
				self._logger.info("Couldn't connect to the FilaWeigher. Will try again in 60s")
				self.t.cancel()
				self.t = octoprint.util.RepeatedTimer(120.0, self.check_sensors)
				self.t.start()		 
		else: #if it's not a valid IP address, turn off the timer. The timer gets turned back on
				# whenever settings are saved. 
			self._logger.info("'" + IPAddress + "' is not a valid IP Address")
			self.t.cancel()

#This just restarts the timer when the settings are saved. In case it got turned off 
# due to bad settings. 
	def on_settings_save(self,data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
		try:
			self.t = octoprint.util.RepeatedTimer(5.0, self.check_sensors)
			self.t.start()
		except:
			self._logger.info("Couldn't start the timer. Might be running already")

#function to check if the IP Address setting is a valid IP address. 
	def is_valid_ipv4_address(self,address):
		try:
			socket.inet_pton(socket.AF_INET, address)
		except AttributeError:  # no inet_pton here, sorry
			try:
				socket.inet_aton(address)
			except socket.error:
				return False
			return address.count('.') == 3
		except socket.error:  # not a valid address
			return False

		return True			

#This defines info for plugin updates. 
	def get_update_information(self):
		return dict(
			filaweigher=dict(
				displayName="OctoPrint FilaWeigher",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="simpat1zq",
				repo="OctoPrint-FilaWeigher",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/simpat1zq/OctoPrint-FilaWeigher/archive/{target_version}.zip"
			)
		)



# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "OctoPrint FilaWeigher"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = filaweigherPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

