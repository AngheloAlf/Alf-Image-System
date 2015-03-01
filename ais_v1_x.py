## Alf Image System
##
## History:
## v1.0 indev
## v1.01 filename can be set by command line or by screen now
## v1.02 Update to match how work ais_commons functions
## v1.1 add encript system
##

version = 1.1
print "Loading Alf Image System v"+str(version)+" ..."
import sys, os, Image, ais_commons
formats = ais_commons.formats

def get_color_pixels(RGB):
	pixels = {}
	contadorx = 0
	for i in RGB:
		contadory = 0
		for j in i:
			if j in pixels:
				pixels[j].append((contadorx,contadory))
			else:
				pixels[j] = [(contadorx,contadory)]
			contadory+=1
		contadorx +=1
	return pixels

def write_ais_pixels(nombre, pixels, nombre_destino = None, encript_number = False):
	encript = False
	if type(encript_number) == int or encript_number:
		encript = True
	if nombre_destino == None:
		ais_file = open(nombre.split(".")[0]+".ais","a")
	else:
		nombre_destino = nombre_destino.split(".")
		ais_file = open(nombre_destino[0]+".ais","a")
	ais_file.write("ALF\n")
	for color in pixels:
		pixels_color = str(pixels[color])[1:-1]
		color = str(color)[1:-1]
		if encript:
			color = ais_commons.encript(color,encript_number)
			pixels_color = ais_commons.encript(pixels_color,encript_number)
		ais_file.write(color+" = "+pixels_color+"\n")
	ais_file.close()
	print "done"
	return

def get_ais_pixels(nombre, ais_data, encript_number = False):
	encript = False
	if type(encript_number) == int or encript_number:
		encript = True
	try:
		ais_file = open(nombre)
	except:
		print "AIS file not found"
		exit()
	if ais_data[0]<1.0:
		print "This AIS file it's not compatible with this software, please get the correct version"
		exit()
	ais_pixels = {}
	pixel = False
	for line in ais_file:
		if line.strip() == "ALF":
			pixel = True
			continue
		if pixel:
			line = line.strip().split(" = ")
			if encript:
				line[0] = ais_commons.de_encript(line[0],encript_number)
				line[1] = ais_commons.de_encript(line[1],encript_number)
			lista = []
			for i in line[1].split("), ("):
				cosa = tuple(map(int,i.strip("(").strip(")").split(", ")))
				lista.append(cosa)
			ais_pixels[tuple(map(int,(line[0].split(", "))))] = lista
	return ais_pixels

def create_image(nombre, ais_data,ais_pixels):
	print "Creating image file as: "+nombre
	image_file = Image.new("RGB",ais_data[4])
	pix = image_file.load()
	for RGB in ais_pixels:
		for pos in ais_pixels[RGB]:
			pix[pos] = RGB
	image_file.save(nombre, ais_data[3])
	return

def ais_main_1_x(name = None, toname = None, arguments = []):
	extra_arguments = ais_commons.comands_arguments(arguments)
	nombre, nombre_destino = ais_commons.resolve_name(name,toname,extra_arguments)

	if nombre.split(".")[1]!="ais":
		image = ais_commons.open_image(nombre)
		RGB = ais_commons.get_RGB_list(image)
		pixels = get_color_pixels(RGB)
		ais_commons.create_ais_file(nombre,image.size,current_version = version)
		write_ais_pixels(nombre,pixels)
	else:
		ais_data = ais_commons.read_ais_head(nombre)
		ais_pixels = get_ais_pixels(nombre,ais_data)
		create_image(ais_data[2], ais_data,ais_pixels)
	return 0

print "AIS v"+str(version)+" loading done"

if __name__ == "__main__":
	error = ais_main_1_x("test.ais")
	if error:
		print "The program has finished with error code "+str(error)

#E.O.F End of file