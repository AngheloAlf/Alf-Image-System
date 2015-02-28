## Alf random image system :D

from ais import *
import random
import sys

x,y = None,None
for i in sys.argv[1:]:
	i = i.split("=")
	if i[0] == "-x":
		try:
			x = str(int(i[1]))
		except:
			print "Invalid x value"
	if i[0] == "-y":
		try:
			y = str(int(i[1]))
		except:
			print "Invalid y value"
if not x:
	x = raw_input("x: ")
if not y:
	y = raw_input("y: ")
create_ais_file("Random.png",(int(x),int(y)))
ais_file = open("Random.ais","a")
ais_file.write("ALF\n")
print "Making Random Image "+x+"*"+y
print "0.0%  completado"
x = int(x)
y = int(y)
porcen = 0
for i in range(x):
	linea = ""
	for j in range(y):
		linea += "40."
		for algo in range(3):
			random_pixel = str(random.randint(0,255))
			for k in random_pixel:
				linea += str(ord(k))+"."
			if algo <2:
				linea += "44.32."
			else:
				linea += "41"
		linea += ".44.32."
	linea = de_encript(linea[:-7],0)
	ais_file.write(linea+"\n")
	porcen_act = float(i)*100.0/float(x)
	if int(porcen_act) > porcen:
		print str(porcen_act)+"%  completado"
		porcen = porcen_act
ais_file.close()

ais_data = read_ais_head("Random.ais")
ais_pixels = open_ais_file("Random.ais",ais_data)
create_image_file(ais_data[2],ais_data[4],ais_pixels,ais_data[3])