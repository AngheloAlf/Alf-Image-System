## Alf Image System Commons
##
## History:
## v0.1 First version
## v0.11 More functions
## v0.12 little change 
##

version_commons = 0.11
print "Loading Commons v"+str(version_commons)+" ..."
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
	#pix[x,y] = value # Set the RGBA Value of the image (tuple)
	return RGB

def create_ais_file(nombre,dim_imagen,nombre_destino = None,encript_number = None,current_version = version_commons):
	nombre = nombre.split(".")
	if nombre_destino == None:
		print "Saving file as: "+nombre[0]+".ais"
		ais_file = open(nombre[0]+".ais","w")
	else:
		nombre_destino = nombre_destino.split(".")
		if nombre_destino[1].lower() != "ais":
			print "Can't convert image file to image file"
			print "Converting to AIS file"
			print "If you want to convert image file to image file, use a normal image editor"
		print "Saving file as: "+nombre_destino[0]+".ais"
		ais_file = open(nombre_destino[0]+".ais","w")
	ais_file.write(str(current_version)+"\n")
	if encript_number and current_version<1.0:
		ais_file.write("Alf Image System v"+str(current_version)+"e\n")
	else:
		ais_file.write("Alf Image System v"+str(current_version)+"\n")
	ais_file.write(".".join(nombre)+"\n")
	ais_file.write(formats["."+nombre[1]]+"\n")
	ais_file.write(str(dim_imagen)[1:-1]+"\n")
	ais_file.close()
	return

def read_ais_head(nombre):
	try:
	 	print "Loading AIS file: "+nombre
	 	ais_file = open(nombre)
	except:
		print "AIS file not found"
		exit()
	ais_data = []
	for linea in ais_file:
		ais_data.append(linea.strip())
		if linea.strip() == "ALF":
			ais_data[4] = tuple(map(int,ais_data[4].split(", ")))
			ais_data[0] = float(ais_data[0])
			if ais_data[1][-1] == "e":
				ais_data[5] = int(ais_data[5])
			break
	return ais_data

def comands_arguments(arguments = []):
	##Commands:
	##"--name" or "-n" = name of the file
	##"--toname" or "-tn" = name of the destiny filename
	##"--verify" or "-v" = verify after the creation of the AIS file
	##"--only-verify" or "-ov" = only verify the ais file with the image file and close the program
	##"--do-nothing" or "-no" = do nothing
	##"--encript" or "-e" = encript or decript the AIS file
	##"--only-encript" or "-oe" = only encript or decript de AIS file
	nombre = None
	nombre_destino = None
	arguments_list = sys.argv[1:] + arguments
	extra_arguments = {"verify":False,"only-verify":False,"do-nothing":False,"encript": None,"only-encript":None,"-x":None,"-y":None}
	for argument in arguments_list:
		good_argument = False
		argument = argument.split("=")
		if argument[0] == "-n" or argument[0] == "--name":
			argument_line = argument[1].split(".")
			if len(argument_line)>1 and "."+argument_line[1] in formats:
				nombre = argument[1]
				good_argument = True
		if argument[0] == "-tn" or argument[0] == "--toname":
			argument_line = argument[1].split(".")
			if len(argument_line)>1 and "."+argument_line[1] in formats:
				if argument[1] != nombre:
					nombre_destino = argument[1]
					good_argument = True
		if argument[0] == "-v" or argument[0] == "--verify":
			extra_arguments["verify"] = True
			good_argument = True
		if argument[0] == "-ov" or argument[0] == "--only-verify":
			extra_arguments["only-verify"] = True
			good_argument = True
		if argument[0] == "-no" or argument[0] == "--do-nothing":
			extra_arguments["do-nothing"] = True
			good_argument = True
		if argument[0] == "-e" or argument[0] == "--encript":
			if len(argument)>1:
				extra_arguments["encript"] = int(argument[1])
			else:
				extra_arguments["encript"] = True
			good_argument = True
		if argument[0] == "-oe" or argument[0] == "--only-encript":
			if len(argument)>1:
				extra_arguments["only-encript"] = int(argument[1])
			else:
				extra_arguments["only-encript"] = True
			good_argument = True
		if argument[0] == "-x":
			extra_arguments["-x"] = argument[1]
			good_argument = True
		if argument[0] == "-y":
			print argument
			extra_arguments["-y"] = argument[1]
			good_argument = True
		if not good_argument:
			print "The argument '"+ argument[0]+ "' it's not a valid argument or you are using it wrong"
	return nombre,nombre_destino,extra_arguments

def encript(linea,cod = 211):
	coded = []
	for i in linea:
		coded.append(str(ord(i)+cod))
	return ".".join(coded)

def de_encript(linea,cod = 211):
	decoded = ""
	for i in linea.split("."):
		decoded += str(chr(int(i)-cod))
	return decoded

print "Commons loading done"

#E.O.F End of file