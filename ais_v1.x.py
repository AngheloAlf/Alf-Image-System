## Alf Image System
##
## History:
## v1.0 indev
##

version = 1.0
print "Loading Alf Image System v"+str(version)+" ..."
import sys, os, Image, ais_commons
formats = ais_commons.formats

def get_color_pixels(RGB):
	pixels = {}
	contadorx = 0
	for i in RGB:
		contadory = 0
		contadorx +=1
		for j in i:
			contadory+=1
			if j in pixels:
				pixels[j].append((contadorx,contadory))
			else:
				pixels[j] = [(contadorx,contadory)]
	return pixels

def write_ais_pixels(nombre,pixels,nombre_destino = None):
	if nombre_destino == None:
		ais_file = open(nombre.split(".")[0]+".ais","a")
	else:
		nombre_destino = nombre_destino.split(".")
		ais_file = open(nombre_destino[0]+".ais","a")
	ais_file.write("ALF\n")
	for color in pixels:
		ais_file.write(str(color)[1:-1]+" = "+str(pixels[color])[1:-1]+"\n")
	ais_file.close()
	print "done"
	return



def ais_main_1_x():
	nombre = "test.png"
	image = ais_commons.open_image(nombre)
	RGB = ais_commons.get_RGB_list(image)
	pixels = get_color_pixels(RGB)
	ais_commons.create_ais_file(nombre,image.size,current_version = version)
	write_ais_pixels(nombre,pixels)
	return

print "AIS v"+str(version)+" loading done"

ais_main_1_x()

#E.O.F End of file