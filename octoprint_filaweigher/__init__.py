# coding=utf-8
from __future__ import absolute_import
import sys


import octoprint.plugin
import flask
import threading
import urllib2
import socket


class filaweigherPlugin(octoprint.plugin.SettingsPlugin,
						   octoprint.plugin.AssetPlugin,
						   octoprint.plugin.TemplatePlugin,
						   octoprint.plugin.StartupPlugin):

	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=True)
		]

	def get_settings_defaults(self):
		return dict(
			filaweigherIP=["Enter FilaWeigher IP here"],
		)

	def get_assets(self):
		return dict(
			js=["js/filaweigher.js"],
			css=["css/filaweigher.css"],
			less=["less/filaweigher.less"]
		)

	def on_startup(self, host, port):
		self.number = 0
		self.t = octoprint.util.RepeatedTimer(5.0, self.check_sensors)
		self.t.start()

	def check_sensors(self):
		# url = "http://192.168.45.108/json"
		IPAddress = self._settings.get(["filaweigherIP"])[0]
		if self.is_valid_ipv4_address(IPAddress):
			url = "http://" + self._settings.get(["filaweigherIP"])[0] + "/json"
			self._logger.info(url)
			try:
				page = urllib2.urlopen(url)
				self._plugin_manager.send_plugin_message(self._identifier, page.read())
			except:
				self._logger("Couldn't connect to the FilaWeigher")
			 
		else:
			self._logger.info("'" + IPAddress + "' is not a valid IP Address")
			self.t.cancel()

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

	def on_settings_save(self):
		try:
			self.t.start()
		except:
			self._logger.info("Couldn't start the timer. Might be running already")


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

