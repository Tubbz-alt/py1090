import sys, os.path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

import py1090 
		
def record_positions_to_file(filename):
	with py1090.Connection('192.168.10.2') as connection:
		lines = 0
		for line in connection:
			message = py1090.Message.from_string(line)
			if message.latitude and message.longitude:
				print(line)
				lines += 1			

if __name__ == "__main__":
	record_positions_to_file("example_recording.txt")
	