$(function() {
    function filaweigherViewModel(parameters) {
        var self = this;
		self.printerState = parameters[0]
		self.settings = parameters[1]

		//sets the 4 sensors to 'loading'. It will show this until we get a reading from 
		// the filaweigher 
		self.printerState.filamentRemainingString = ko.observable("Loading...")
		self.printerState.temperatureString = ko.observable("Loading...")
		self.printerState.humidityString = ko.observable("Loading...")
		//self.printerState.pressureString = ko.observable("Loading...")

		//when __init.py sends a plugin message, this function kicks into action
		self.onDataUpdaterPluginMessage = function(plugin, message){
			if (plugin != "filaweigher") return; //stop if the message wasn't from the filaweigher plugin
			var obj = JSON.parse(message); //parse the json and load it into obj
			//set all the sensor values 
			self.printerState.filamentRemainingString(obj.weight + "g"); 
			self.printerState.temperatureString(obj.temperature + "%");
			self.printerState.humidityString(obj.humidity + "C");
			//self.printerState.pressureString(obj.pressure); 
	
			console.log(message);
		};

		self.onStartup = function() {
			//This displays all the sensor readings in the gui right after the printer state
			// on the left side
			var element = $("#state").find(".accordion-inner [data-bind='text: stateString']");
            if (element.length) {
                //var text = gettext("Filament Remaining");
				element.after("<br>Printer Humidity: <strong data-bind='text: humidityString'></strong>");
				element.after("<br>Printer Temperature: <strong data-bind='text: temperatureString'></strong>");
		    		element.after("<br>Filament Remaining: <strong data-bind='text: filamentRemainingString'></strong>");
				//element.after("<br>Pressure: <strong data-bind='text: pressureString'></strong>");
            }
        };
	}

    OCTOPRINT_VIEWMODELS.push({
        construct: filaweigherViewModel,
        dependencies: ["printerStateViewModel", "settingsViewModel"],
        elements: ["#settings_plugin_filaweigher"]
    });
});
