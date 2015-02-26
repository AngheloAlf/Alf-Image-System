from ais import *
import random
import sys

ais_file = open("Random.ais","w")
ais_file.write(str(version)+"\n")
ais_file.write("Alf Image System v"+str(version)+"\n")
ais_file.write("Random.png"+"\n")
ais_file.write("PNG"+"\n")
if len(sys.argv)>2:
	x,y = sys.argv[1],sys.argv[2]
else:
	x = raw_input("x: ")
	y = raw_input("y: ")
ais_file.write(x+", "+y+"\n")
ais_file.write("ALF\n")
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

ais_data,ais_pixels = open_ais_file("Random.ais")
create_image_file(ais_data[2],ais_data[4],ais_pixels,ais_data[3])