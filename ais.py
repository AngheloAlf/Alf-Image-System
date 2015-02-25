## Alf Image System
## History:
## v0.1 First version
## v0.2 Added command naming functions
##

version = 0.21
print "Loading..."
import sys, os, Image

formats = {".bmp": "BMP",".gif":"GIF",".jfif":"JPEG",".jpe":"JPEG",".jpg":"JPEG",".jpg":"JPEG",".png":"PNG",".pbm":"PPM",".pgm":"PPM",".ppm":"PPM",".ais":"AIS"}

def open_image(nombre):
	try:
		print "Loading image file: "+nombre
		return Image.open(os.path.join(nombre))
	except:
		print "Error loading the image"
		exit()
		return None

def get_RGB_list(imagen, inicio = (0,0), final = (0,0), seccion = False):
	print "Loading RGB"
	pix = imagen.load() ##carga los pixeles de la imagen
	#imagen.rotate(180).save(nombre+"_rotada.jpg", "JPEG")##rota la imagen
	dim_imagen = imagen.size #entrega el largo de la imagen como una tupla (x,y)
	RGB = [] ##lista donde se almacenara el RGB
	RGBy = []
	for x in range(dim_imagen[0]): ##recorre la coordenada X de la imagen
		if seccion and (inicio[0]>x or final[0]<x): #para saltar secciones de la imagen
			continue
		for y in range(dim_imagen[1]): ##recorre la coordenada Y de la imagen
			if seccion and (inicio[1]>y or final[1]<y): #para saltar secciones de la imagen
				continue
			RGBy.append(pix[x,y])##almacena los colores RGB de la imagen
		RGB.append(RGBy)
		RGBy = []
		#completado = x*100.0/dim_imagen[0] #
	#pix[x,y] = value # Set the RGBA Value of the image (tuple)
	return RGB

def write_ais_file(nombre, RGB, dim_imagen, nombre_destino = None):
	nombre = nombre.split(".")
	if nombre_destino == None:
		print "Saving file as: "+nombre[0]+".ais"
		ais_file = open(nombre[0]+".ais","w")
	else:
		print nombre_destino
		nombre_destino = nombre_destino.split(".")
		if nombre_destino[1].lower() != "ais":
			print "Can't convert image file to image file"
			print "Converting to AIS file"
			print "If you want to convert image file to image file, use a normal image editor"
		print "Saving file as: "+nombre_destino[0]+".ais"
		ais_file = open(nombre_destino[0]+".ais","w")
	ais_file.write(str(version)+"\n")
	ais_file.write("Alf Image System v"+str(version)+"\n")
	ais_file.write(".".join(nombre)+"\n")
	ais_file.write(formats["."+nombre[1]]+"\n")
	ais_file.write(str(dim_imagen)[1:-1]+"\n")
	ais_file.write("ALF\n")
	for i in RGB:
		i = str(i)[1:-1]
		ais_file.write(i)
		ais_file.write("\n")
	ais_file.close()
	return 

def open_ais_file(nombre):
	try:
		print "Loading AIS file: "+nombre
		ais_file = open(nombre)
	except:
		print "AIS file not found"
		exit()
	ais_data = []
	ais_pixels = []
	inicio = True
	for linea in ais_file:
		if inicio:
			ais_data.append(linea.strip())
			if linea.strip() == "ALF":
				inicio = False
			continue
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
	ais_data[4] = tuple(map(int,ais_data[4].split(", ")))
	return ais_data,ais_pixels

def create_image_file(nombre,dim_imagen,ais_pixels,codificacion):
	print "Creating image file as: "+nombre
	image_file = Image.new("RGB",dim_imagen)
	pix = image_file.load()
	for x in range(dim_imagen[0]):
		for y in range(dim_imagen[1]):
			pix[x,y] = ais_pixels[x][y]
	image_file.save(nombre, codificacion)
	return

def comands_arguments():
	contador = 0
	nombre = None
	nombre_destino = None
	Name = False
	toName = False
	for argument in sys.argv[1:]:
		if contador == 0:
			argument_line = argument.split(".")
			if len(argument_line)>1 and "."+argument_line[1] in formats:
				nombre = argument
				Name = True
		if contador == 1 and Name:
			argument_line = argument.split(".")
			if len(argument_line)>1 and "."+argument_line[1] in formats:
				if argument != nombre:
					nombre_destino = argument
					toName = True
		contador+=1
	#if Name and not toName:
	#	nombre_destino = nombre
	return nombre,nombre_destino


nombre,nombre_destino = comands_arguments()

if nombre == None:
	nombre = raw_input("Nombre del archivo: ")
	nombre_destino = raw_input("Nombre del archivo de destino (dejar en blanco para nombre automatico): ")
	if nombre_destino == "":
		nombre_destino = None
if "."+nombre.split(".")[1].lower() not in formats:
	print "The file is not an image"
	exit()

if "."+nombre.split(".")[1].lower() != ".ais":
	imagen_cargada = open_image(nombre)
	RGB = get_RGB_list(imagen_cargada)
	if nombre_destino == None:
		write_ais_file(nombre, RGB, imagen_cargada.size)
	else:
		write_ais_file(nombre, RGB, imagen_cargada.size, nombre_destino)
else:
	ais_data,ais_pixels = open_ais_file(nombre)
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

# print tuple(map(int,ais_data[4].split(", "))) == dim_imagen
# print ais_data[2] == nombre
# print ais_pixels == RGB