# coding=utf-8
from __future__ import absolute_import
import sys


import octoprint.plugin
import flask
import threading


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
			weight-topic = "your/weight/topic",
			temperature-topic = "your/temperature/topic",
			humidity-topic = "your/humidity/topic",
			pressure-topic = "your/pressure/topic" 
		)

	def get_assets(self):
		return dict(
			js=["js/filaweigher.js"],
			css=["css/filaweigher.css"],
			less=["less/filaweigher.less"]
		)

	
	def on_startup(self, host, port):
		self.t = octoprint.util.RepeatedTimer(3.0, self.check_sensors)
		self.t.start()
		
	def check_sensors(self):
		self.hx.power_up()
		v = self.hx.read()
		self._plugin_manager.send_plugin_message(self._identifier, v) 
		self.hx.power_down()
		
	def get_update_information(self):

		return dict(
			filament_scale=dict(
				displayName="OctoPrint FilaWeigher",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="simpat1zq",
				repo="OctoPrint-FilaWeigher",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/dieki-n/OctoPrint-Filament-scale/archive/{target_version}.zip"
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
		"octoprint.plugin5.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

