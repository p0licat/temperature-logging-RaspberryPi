import Adafruit_DHT
import mariadb
import sys
import datetime
import time

sensor = Adafruit_DHT.AM2302

pin = 23

# flags
read_counts = None # set to number of reads, or None if permanent
# end flags

conn = None

try:
	conn = mariadb.connect(
		user="[xxx]",
		password="[xxx]",
		host="192.168.0.x",
		port=3306)
except mariadb.Error as e:
	print("error")	
	sys.exit(0)
	
cur = conn.cursor()
cur.execute("USE temperature_data")

while (read_counts is not None and read_counts > 0) or (read_counts is None):
	
	time.sleep(3) # seconds
	
	try_counts = 4
	hist_tuples = []
	while try_counts > 0:
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		time.sleep(1)
		hist_tuples.append((humidity, temperature))
		if humidity is not None and temperature is not None:
			try_counts -= 1
	
	passed_tuples = []
	for i in range(len(hist_tuples) - 1):
		if hist_tuples[i][0] - hist_tuples[i+1][0] > 10. or hist_tuples[i][1] - hist_tuples[i+1][1] > 10.:
				print("b1")
				continue
		else:
			passed_tuples.append(hist_tuples[i])
	if len(passed_tuples) == 0:
		print("b2")
		continue
	
	humidity, temperature = passed_tuples[0]
	
	time_now = datetime.datetime.now()
	print(type(humidity))
	print(type(temperature))
	
	try:
		cur.execute("INSERT INTO mainroomlog SET temp_value={0:0.1f}, datetime_cap=\"{1}\", humidity={2:0.1f}".format(
			temperature, 
			time_now.strftime("%Y-%m-%d %H:%M:%S"),
			humidity
		))
	except mariadb.DatabaseError as err:
		try:
			conn.reconnect()
			cur.execute("USE temperature_data")
		except:
			continue
	except Exception as ex:
		print(ex)
		read_counts = 0
		continue
	
	if humidity is not None and temperature is not None:
		print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
	else:
		print('Failed to get reading. Try again!')
	
	
	if (read_counts is not None):
		read_counts -= 1
	

conn.close()
