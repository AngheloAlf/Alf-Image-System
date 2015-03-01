## Alf Image System
##
## History:
## v0.1 First version
## v0.2 Added command naming functions
## v0.21 minor fix
## v0.22 Added verify_integrity function
## v0.3 Add encript system
## v0.31 best command line encript system
## v0.32 ais_main added
## v0.33 AIS head creator function
## v0.34 add compativility with ais_commons
## v0.35 add compativility with ais_commons.resolve_name
## v0.36 Update to match how work ais_commons functions
## v0.361 little clean up
## v0.4 Add errors codes
##

version = 0.4
print "Loading Alf Image System v"+str(version)+" ..."
import sys, os, Image, ais_commons
formats = ais_commons.formats
errors_codes = ais_commons.errors_codes

def write_ais_file(nombre, RGB, nombre_destino = None, encript_number = None):
	nombre = nombre.split(".")
	if nombre_destino == None:
		ais_file = open(nombre[0]+".ais","a")
	else:
		nombre_destino = nombre_destino.split(".")
		ais_file = open(nombre_destino[0]+".ais","a")
	if encript_number != None:
		print "Encripting"
		ais_file.write(str(encript_number)+"\n")
	ais_file.write("ALF\n")
	for i in RGB:
		i = str(i)[1:-1]
		if encript_number == None:
			ais_file.write(i)
		else:
			ais_file.write(ais_commons.encript(i,encript_number))
		ais_file.write("\n")
	ais_file.close()
	print "Save successful"
	return 

def open_ais_file(nombre,ais_data,decript_number=None):
	try:
		ais_file = open(nombre)
	except:
		return 4
	if ais_data[0]>=1.0:
		return 5
	ais_pixels = []
	pixels = False
	encripted = False
	if ais_data[1][-1] == "e":
		encripted = True
	for linea in ais_file:
		if linea.strip() == "ALF":
			pixels = True
			continue
		if pixels:
			if encripted:
				if decript_number == None:
					return 7
				if decript_number != ais_data[5]:
					return 6
				linea = ais_commons.de_encript(linea,decript_number)
			fla = linea.strip().split("), ")
			rgb_linea = []
			for iteracion in fla:
				#se que esto se puede hacer en una linea
				#pero lo esta asi porque asi va a ser mas entendible
				#si algun dia tengo que volver a leer lo que escribi aqui
				iteracion = iteracion[1:].strip(")")
				iteracion = iteracion.split(", ")
				iteracion = map(int,iteracion)
				iteracion = tuple(iteracion)
				rgb_linea.append(iteracion)
			ais_pixels.append(rgb_linea)
	ais_file.close()
	return ais_pixels

def create_image_file(nombre,dim_imagen,ais_pixels,codificacion):
	print "Creating image file as: "+nombre
	image_file = Image.new("RGB",dim_imagen)
	pix = image_file.load()
	for x in range(dim_imagen[0]):
		for y in range(dim_imagen[1]):
			pix[x,y] = ais_pixels[x][y]
	image_file.save(nombre, codificacion)
	print "Save successful"
	return

def verify_integrity(nombre, dim_imagen = None, RGB = None, nombre_destino = None, only = False,decript_number = None):
	print "Loading files"
	if only:
		image = ais_commons.open_image(nombre)
		if type(image) == int:
			return image
		RGB = ais_commons.get_RGB_list(image)
		dim_imagen = image.size
	if nombre_destino == None:
		nombre_destino = nombre
	ais_data = ais_commons.read_ais_head(nombre_destino.split(".")[0]+".ais")
	if type(ais_data) == int:
		return ais_data
	ais_pixels = open_ais_file(nombre_destino.split(".")[0]+".ais",ais_data,decript_number)
	if type(ais_pixels) == int:
		return ais_pixels
	print "Verifing integrity"
	print "Name: "+ str(ais_data[2] == nombre)
	print "Image resolution: "+ str(ais_data[4] == dim_imagen)
	print "Pixel per pixel verification: "+ str(ais_pixels == RGB)
	if ais_data[2] == nombre and ais_data[4] == dim_imagen and ais_pixels == RGB:
		print "Everything looks good :D"
	else:
		print "Something go wrong :c"
	return 0

def ais_main_v0_x(name = None, toname = None, arguments = []):
	extra_arguments = ais_commons.comands_arguments(arguments)
	if extra_arguments["-no"]:
		print "Doing nothing"
		return 0
	nombre, nombre_destino = ais_commons.resolve_name(name,toname,extra_arguments)

	if type(nombre) == int:
		return nombre 

	if extra_arguments["-e"] == True:
		extra_arguments["-e"] = 211
	if extra_arguments["-oe"]== True:
		extra_arguments["-oe"] = 211

	if extra_arguments["-oe"] != None:
		ais_data = ais_commons.read_ais_head(nombre)
		if type(ais_data) == int:
			return ais_data
		ais_pixels = open_ais_file(nombre,ais_data,extra_arguments["-oe"])
		if type(ais_pixels) == int:
			return ais_pixels
		ais_commons.create_ais_file(nombre,ais_data[4],nombre_destino,extra_arguments["-oe"],version)
		write_ais_file(ais_data[2], ais_pixels, nombre_destino, extra_arguments["-oe"])
		return 0

	if extra_arguments["-ov"]:
		if nombre and nombre_destino:
			error = verify_integrity(nombre,nombre_destino = nombre_destino,only = True,decript_number = extra_arguments["-e"])
			return error
		else:
			return 2

	if "."+nombre.split(".")[1].lower() != ".ais":
		imagen_cargada = ais_commons.open_image(nombre)
		if type(imagen_cargada) == int:
			return imagen_cargada
		RGB = ais_commons.get_RGB_list(imagen_cargada)
		ais_commons.create_ais_file(nombre,imagen_cargada.size,nombre_destino,extra_arguments["-e"],version)
		write_ais_file(nombre, RGB, nombre_destino, extra_arguments["-e"])
		if extra_arguments["-v"]:
			verify_integrity(nombre,imagen_cargada.size,RGB,nombre_destino,decript_number = extra_arguments["-e"])
	else:
		ais_data = ais_commons.read_ais_head(nombre)
		if type(ais_data) == int:
			return ais_data
		ais_pixels = open_ais_file(nombre,ais_data,extra_arguments["-e"])
		if type(ais_pixels) == int:
			return ais_pixels

		if nombre_destino != None:
			if nombre_destino.split(".")[1].lower() != "ais":
				codificacion = formats["."+nombre_destino.split(".")[1]]
			else:
				print "Can't convert AIS file to AIS file"
				print "Using predetermined name and format of the AIS file"
		if nombre_destino == None or nombre_destino.split(".")[1].lower() == "ais":
			nombre_destino = ais_data[2]
			codificacion = ais_data[3]
		create_image_file(nombre_destino,ais_data[4],ais_pixels,codificacion)

	return 0

print "Load done"

if __name__== "__main__":
	error = ais_main_v0_x()
	if error:
		print "The program has finished with error code "+str(error)
		print "-- "+errors_codes[error]+" --"

#E.O.F End of file