$(function() {
    function filaweigherViewModel(parameters) {
        var self = this;
		self.printerState = parameters[0]
		self.settings = parameters[1]
 
		self.printerState.filamentRemainingString = ko.observable("Loading...")
		self.printerState.temperatureString = ko.observable("Loading...")
		self.printerState.humidityString = ko.observable("Loading...")
		self.printerState.pressureString = ko.observable("Loading...")

		self.onDataUpdaterPluginMessage = function(plugin, message){
			if (plugin != "filaweigher") return;
			var obj = JSON.parse(message); 

			self.printerState.filamentRemainingString(obj.weight + "g");	
			self.printerState.temperatureString(obj.temperature);
			self.printerState.humidityString(obj.humidity);
			self.printerState.pressureString(obj.pressure); 
	
			console.log(message);
		};

		self.onStartup = function() {
			var element = $("#state").find(".accordion-inner [data-bind='text: stateString']");

            if (element.length) {
                //var text = gettext("Filament Remaining");
				element.after("<br>Filament Remaining: <strong data-bind='text: filamentRemainingString'></strong>");
				element.after("<br>Room Temperature: <strong data-bind='text: temperatureString'></strong>");
				element.after("<br>Humidity: <strong data-bind='text: humidityString'></strong>");
				element.after("<br>Pressure: <strong data-bind='text: pressureString'></strong>");
            }
        };
	}

    OCTOPRINT_VIEWMODELS.push({
        construct: filaweigherViewModel,
        dependencies: ["printerStateViewModel", "settingsViewModel"],
        elements: ["#settings_plugin_filaweigher"]
    });
});
