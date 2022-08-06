import requests;
def noBattery():
		"""
		sends a post request to the server, telling it that this device has less than 1% of battery.
		"""
		params = {
			"type":"lowBattery",
			"battery":"0"
		};
		x = requests.post("https://script.google.com/macros/s/AKfycbwTPcKwdGHbR4iwxnD_OQ6l6a7v_9f8F9Q0VvPpTN0NLHwln8kGU332h9gp6Wr_Nup3_Q/exec",params=params);
		print(x.text);
		print(x.status_code);
noBattery();
