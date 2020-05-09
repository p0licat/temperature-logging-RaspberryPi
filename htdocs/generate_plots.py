import matplotlib.pyplot as plt
from matplotlib import dates as mpl_dates
import mariadb
import sys
import numpy as np
import datetime
import json


with open("db_config_web.json", "r") as dbj:
    data = dbj.read()
    data = json.loads(data)

username = data["MainConnection"]['username']
password = data["MainConnection"]['password']

try:
    conn = mariadb.connect(
        user=username,
        password=password,
        host="localhost",
        port=3306,
        ssl_ca="C:\\Users\\tbodi\\OneDrive\\Documents\\Code\\MariaDB\\SSL_Certs\\ca.pem")
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()
cur.execute("USE home_sensors")

# 1. find current time and date

now = datetime.datetime.now() + datetime.timedelta(days=1)  # + needed for LT
yday = now - datetime.timedelta(days=2)
#  print(now.strftime("%Y-%m-%d"))
#  print( (yday).strftime("%Y-%m-%d") )
# 2. Select/Get all entries for last 2 days
cur.execute("SELECT * FROM temperature_humidity WHERE measurement_date BETWEEN \"{0}\" AND \"{1}\"".format(
    yday.strftime("%Y-%m-%d"),
    now.strftime("%Y-%m-%d")
))

# 3. Generate humidity and temperature plots

# data parsing
temps = []
hums = []

for item in cur:
    temp_tup = (item[1], item[2])  # temp, time
    hum_tup = (item[3], item[2])  # hum, time
    temps.append(temp_tup)
    hums.append(hum_tup)
# end data parsing

# p1
x_axis = [i[1] for i in temps]
y_axis = [temp[0] for temp in temps]

try:
    ymax = max(y_axis)
    ymin = min(y_axis)

    plt.plot_date(x_axis, y_axis, linestyle='-', marker=',', color='red')
    plt.gcf().autofmt_xdate()  # get current figure
    date_format = mpl_dates.DateFormatter('%b-%d, %H:%M:%S')
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.ylim(top=ymax + 8, bottom=ymin - 3)
    plt.yticks(np.arange(ymin - 3, ymax + 8, step=1))
    plt.gca().tick_params(labelright=True)

    plt.ylabel = "Temperaturi ultimele 2 zile"
    plt.xlabel = "Timpul masurarii"

    plt.savefig("p1.png")

    plt.clf()
except Exception:
    conn.close()
    sys.exit(0)

# p2

x_axis = [i[1] for i in hums]
y_axis = [temp[0] for temp in hums]

try:
    ymax = max(y_axis)
    ymin = min(y_axis)

    plt.plot_date(x_axis, y_axis, linestyle='-', marker=',', color='blue')
    plt.gcf().autofmt_xdate()  # get current figure
    date_format = mpl_dates.DateFormatter('%b-%d, %H:%M:%S')
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.ylim(top=ymax + 4, bottom=ymin - 4)
    plt.yticks(np.arange(ymin - 4, ymax + 4, step=2))
    plt.gca().tick_params(labelright=True)

    plt.ylabel = "Umiditate relativa (%) ultimele 2 zile"
    plt.xlabel = "Timpul masurarii"

    plt.savefig("p2.png")

    plt.clf()
except Exception:
    conn.close()
    sys.exit(0)

conn.close()

# generate and print average tmemps as exit code


def ParagraphWrap(string):
    ptago = '<p>'
    ptagc = '</p>'

    return ptago + string + ptagc


avg_temp = 0
avg_hum = 0

for i in temps:
    avg_temp += i[0]
avg_temp /= len(temps)

for i in hums:
    avg_hum += i[0]
avg_hum /= len(hums)

print(ParagraphWrap("Temperatura medie: {0:0.1f} C".format(avg_temp)))
print(ParagraphWrap("Umiditate medie: {0:0.1f}%".format(avg_hum) + " rh"))
