import sys
import os
import Image

formats = {".bmp": "BMP",".gif":"GIF",".jfif":"JPEG",".jpe":"JPEG",".jpg":"JPEG",".jpg":"JPEG",".png":"PNG",".pbm":"PPM",".pgm":"PPM",".ppm":"PPM",".ais":"AIS"}
nombre = None
try:
	if sys.argv[1] != "":
		nombre = sys.argv[1]
except:
	pass

def open_image(nombre):
	try:
		return Image.open(os.path.join(nombre))
	except:
		print "Error loading the image"
		exit()
		return None

def get_RGB_list(imagen, inicio = (0,0), final = (0,0), seccion = False):
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

def write_ais_file(nombre, RGB, dim_imagen):
	nombre = nombre.split(".")
	print nombre
	ais_file = open(nombre[0]+".ais","w")
	ais_file.write("0.1\n")
	ais_file.write("Alf Image System v0.1\n")
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
	ais_file = open(nombre)
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
	image_file = Image.new("RGB",dim_imagen)
	pix = image_file.load()
	for x in range(dim_imagen[0]):
		for y in range(dim_imagen[1]):
			pix[x,y] = ais_pixels[x][y]
	image_file.save(nombre, codificacion)
	return


if nombre == None:
	nombre = raw_input("nombre del archivo: ")
if "."+nombre.split(".")[1].lower() not in formats:
	print "The file is not an image"
	exit()
if "."+nombre.split(".")[1].lower() != ".ais":
	imagen_cargada = open_image(nombre)
	RGB = get_RGB_list(imagen_cargada)
	write_ais_file(nombre, RGB, imagen_cargada.size)

else:
	ais_data,ais_pixels = open_ais_file(nombre)
	create_image_file(ais_data[2],ais_data[4],ais_pixels,ais_data[3])

# print tuple(map(int,ais_data[4].split(", "))) == dim_imagen
# print ais_data[2] == nombre
# print ais_pixels == RGB