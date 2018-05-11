import sys, os.path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

import py1090 

def collection_example():
	with py1090.Connection('dvbtadsb') as connection:
		collection = py1090.FlightCollection()
		
		while True:
			print("Number of flights in collection:", len(collection))
			for flight in collection:
				print(flight.callsign," ",flight.flight_id," ",flight.sqwk," ",flight.last_position)
			a=0
			for line in connection:
				message = py1090.Message.from_string(line)
				collection.add(message)
#				print("got msg: ",message)
				if a>10:
					break
				a=a+1

if __name__ == "__main__":
	collection_example()
	