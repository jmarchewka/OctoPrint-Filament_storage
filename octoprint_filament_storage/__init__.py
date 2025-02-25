# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin

class Filament_storagePlugin(octoprint.plugin.SettingsPlugin,
                             octoprint.plugin.AssetPlugin,
                             octoprint.plugin.TemplatePlugin,
                             octoprint.plugin.StartupPlugin):

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			# put your plugin's default settings here
		)

	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/filament_storage.js"],
			css=["css/filament_storage.css"],
			less=["less/filament_storage.less"]
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			filament_storage=dict(
				displayName="Filament_storage Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="jmarchewka",
				repo="OctoPrint-Filament_storage",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/jmarchewka/OctoPrint-Filament_storage/archive/{target_version}.zip"
			)
		)


        def __init__(self):
                self.mqtt_publish = lambda *args, **kwargs: None
                self.mqtt_subscribe = lambda *args, **kwargs: None
                self.mqtt_unsubscribe = lambda *args, **kwargs: None

        def on_after_startup(self):
                helpers = self._plugin_manager.get_helpers("mqtt", "mqtt_publish", "mqtt_subscribe", "mqtt_unsubscribe")
                if helpers:
                        if "mqtt_publish" in helpers:
                                self.mqtt_publish = helpers["mqtt_publish"]
                        if "mqtt_subscribe" in helpers:
                                self.mqtt_subscribe = helpers["mqtt_subscribe"]
                        if "mqtt_unsubscribe" in helpers:
                                self.mqtt_unsubscribe = helpers["mqtt_unsubscribe"]

                self.mqtt_publish("octoprint/plugin/mqtt_test/pub", "test plugin starting up")
                self.mqtt_subscribe("octoprint/plugin/mqtt_test/sub", self._on_mqtt_subscription)

        def _on_mqtt_subscription(self, topic, message, retained=None, qos=None, *args, **kwargs):
                self._logger.info("Yay, received a message for {topic}: {message}".format(**locals()))
                self.mqtt_publish("octoprint/plugin/mqtt_test/pub", "echo: " + message)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Filament_storage Plugin"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
#__plugin_pythoncompat__ = ">=3,<4" # only python 3
#__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = Filament_storagePlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}


