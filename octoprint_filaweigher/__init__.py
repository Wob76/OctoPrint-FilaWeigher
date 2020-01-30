# coding=utf-8
from __future__ import absolute_import
import sys


import octoprint.plugin
import flask
import threading
import urllib2


class filaweigherPlugin(octoprint.plugin.SettingsPlugin,
						   octoprint.plugin.AssetPlugin,
						   octoprint.plugin.TemplatePlugin,
						   octoprint.plugin.StartupPlugin):

	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=True)
		]

	def on_after_startup(self):
		self._logger.info("Hello World!")

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
		url = "http://192.168.45.108/json"
		#url = "http://" + self._settings.get(["filaweigherIP"]) + "/json"
		page = urllib2.urlopen(url)
		self._plugin_manager.send_plugin_message(self._identifier, page.read()) 
		self.number +=  1

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

