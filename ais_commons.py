## Alf Image System Commons
##
## History:
## v0.1 First version
## v0.11 More functions
## v0.12 little change 
## v0.2 add def resolve_name()
## v0.3 change how work def comands_arguments()
## v0.301 litte change
## v0.302 update resolve_name() function
## v0.31 Add errors codes
##

version_commons = 0.4
print "Loading Commons v"+str(version_commons)+" ..."
import sys, os, Image

formats = {".bmp": "BMP",".gif":"GIF",".jfif":"JPEG",".jpe":"JPEG",".jpg":"JPEG",".jpg":"JPEG",".png":"PNG",".pbm":"PPM",".pgm":"PPM",".ppm":"PPM",".ais":"AIS"}
errors_codes = {1:"The filename isn't an image", 2:"You have to put an name and an destiny name to verify integrity", 
3:"The name or the destiny name it's not valid", 4:"File not found",
5:"This AIS file it's not compatible with this software, please get the correct version",
6:"Wrong decript code", 7:"Error reading AIS file"}

def open_image(nombre):
	try:
		print "Loading image file: "+nombre
		return Image.open(os.path.join(nombre))
	except:
		return 4
	return 4

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
		return 4
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
	def resolve_commands(valor):
		extra_arguments[valor] = True
		if len(argument)>1:
			extra_arguments[valor] = argument[1]
		return 
	##Commands:
	##"--name" or "-n" = name of the file
	##"--toname" or "-tn" = name of the destiny filename
	##"--verify" or "-v" = verify after the creation of the AIS file
	##"--only-verify" or "-ov" = only verify the ais file with the image file and close the program
	##"--do-nothing" or "-no" = do nothing
	##"--encript" or "-e" = encript or decript the AIS file
	##"--only-encript" or "-oe" = only encript or decript de AIS file
	##"-x" to give x
	##"-y" to give y
	arguments_list = sys.argv[1:] + arguments
	extra_arguments = {"-n":None, "-tn":None, "-v":False, "-ov":False, "-no":False, 
	"-e": None, "-oe":None, "-x":None, "-y":None}
	alloweds_commands = {"--name":"-n", "--toname":"-tn", "--verify":"-v", 
	"--only-verify": "-ov", "--do-nothing":"-no", "--encript":"-e", 
	"--only-encript": "-oe", "-x":"-x", "-y":"-y"}
	for argument in arguments_list:
		good_argument = False
		argument = argument.split("=")

		if argument[0] in alloweds_commands:
			resolve_commands(alloweds_commands[argument[0]])
			good_argument = True

		if argument[0] in alloweds_commands.values():
			resolve_commands(argument[0])
			good_argument = True

		if not good_argument:
			print "The argument '"+ argument[0]+ "' it's not a valid argument or you are using it wrong"
	return extra_arguments

def encript(linea,cod = 211):
	if cod == True:
		cod = 211
	coded = []
	for i in linea:
		coded.append(str(ord(i)+cod))
	return ".".join(coded)

def de_encript(linea,cod = 211):
	if cod == True:
		cod = 211
	decoded = ""
	for i in linea.split("."):
		decoded += str(chr(int(i)-cod))
	return decoded

def resolve_name(name,toname,extra_arguments):
	nombre,nombre_destino = None,None
	if type(extra_arguments["-n"]) == str:
		nombre = extra_arguments["-n"]
	if type(extra_arguments["-tn"]) == str:
		nombre_destino = extra_arguments["-tn"]

	if name:
		nombre = name
	if toname:
		nombre_destino = toname

	if not nombre:
		nombre = raw_input("Filename: ")
		if not nombre_destino:
			nombre_destino = raw_input("Destiny filename (leave blank to autoname): ")
			if nombre_destino == "":
				nombre_destino = None

	try:
		nombre.split(".")[1]
	except:
		return 3,3
	if nombre_destino:
		try:
			nombre_destino.split(".")[1]
		except:
			return 3,3

	if nombre and nombre_destino:
		if nombre.split(".")[1] == nombre_destino.split(".")[1]:
			nombre_destino = None

	if "."+nombre.split(".")[1].lower() not in formats:
		return 1,1

	return nombre, nombre_destino

print "Commons loading done"

#E.O.F End of file