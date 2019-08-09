import sys, os.path
from datetime import datetime
from influxdb import InfluxDBClient

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

import py1090 

client = InfluxDBClient(host='192.168.10.2', port=8086)
client.switch_database('monitoring')

def record_positions_to_file(filename):
	with py1090.Connection('192.168.10.2') as connection:
		lines = 0
		for line in connection:
			message = py1090.Message.from_string(line)
			if message.latitude and message.longitude:
				#print(line)
				tags={}
				if(message.aircraft_id is not None):
					tags['aircraft_id']=message.aircraft_id
				if(message.callsign is not None):
					tags['callsign']=message.callsign
				if (message.emergency is not None):
					tags['emergency']=message.emergency
				if (message.flight_id is not None):
					tags['flight_id']=message.flight_id
				if (message.hexident is not None):
					tags['hexident']=message.hexident
				if (message.message_type is not None):
					tags['message_type']=message.message_type
				if (message.on_ground is not None):
					tags['on_ground']=message.on_ground
				if (message.session_id is not None):
					tags['session_id']=message.session_id
				if (message.squawk is not None):
					tags['squawk']=message.squawk
				if (message.squawk_alert is not None):
					tags['squawk_alert']=message.squawk_alert
				if (message.spi is not None):
					tags['spi']=message.spi
				if (message.transmission_type is not None):
					tags['transmission_type']=message.transmission_type
				fields={}
				if (message.altitude is not None):
					fields['altitude']= message.altitude
				if (message.ground_speed is not None):
					fields['ground_speed']= message.ground_speed
				if (message.latitude is not None):
					fields['latitude']= message.latitude
				if (message.longitude is not None):
					fields['longitude']= message.longitude
				if (message.track is not None):
					fields['track']= message.track
				if (message.vertical_rate is not None):
					fields['vertical_rate']= message.vertical_rate
				json_body = [
					{
						"measurement": "py1090",
						"tags": tags,
						"time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
						"fields": fields
					}
				]
				print(json_body)
				client.write_points(json_body)
				lines += 1

if __name__ == "__main__":
	record_positions_to_file("example_recording.txt")
	