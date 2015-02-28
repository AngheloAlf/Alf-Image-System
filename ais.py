## Alf Image System
##
## History:
## v0.1 First version
## v0.2 Added command naming functions
## v0.21 minor fix
## v0.22 Added verify_integrity function
## v0.3 Add encript system
## v0.31 best command line encript system
## v0.32 
##

version = 0.32
print "Loading Alf Image System..."
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

def write_ais_file(nombre, RGB, dim_imagen, nombre_destino = None, encript_number = None):
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
	ais_file.write(str(version)+"\n")
	if encript_number == None:
		ais_file.write("Alf Image System v"+str(version)+"\n")
	else:
		ais_file.write("Alf Image System v"+str(version)+"e\n")
	ais_file.write(".".join(nombre)+"\n")
	ais_file.write(formats["."+nombre[1]]+"\n")
	ais_file.write(str(dim_imagen)[1:-1]+"\n")
	if encript_number != None:
		print "Encripting"
		ais_file.write(str(encript_number)+"\n")
	ais_file.write("ALF\n")
	for i in RGB:
		i = str(i)[1:-1]
		if encript_number == None:
			ais_file.write(i)
		else:
			ais_file.write(encript(i,encript_number))
		ais_file.write("\n")
	ais_file.close()
	print "Save successful"
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
			if ais_data[1][-1] == "e":
				ais_data[5] = int(ais_data[5])
			break
	return ais_data

def open_ais_file(nombre,ais_data,decript_number=None):
	try:
		ais_file = open(nombre)
	except:
		print "AIS file not found"
		exit()
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
					print "Error reading AIS file"
					exit()
				if decript_number != ais_data[5]:
					print "Wrong decript code"
					exit()
				linea = de_encript(linea,decript_number)
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
	extra_arguments = {"verify":False,"only-verify":False,"do-nothing":False,"encript": None,"only-encript":None}
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
		if argument[0] == "-no" or argument[0] == "--do-nothing" and true():
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
		if not good_argument:
			print "The argument '"+ argument[0]+ "' it's not a valid argument or you are using it wrong"
	return nombre,nombre_destino,extra_arguments

def true():
	if True:
		return True 
	else:
		return False

def false():
	if not False:
		return False
	else:
		return True

def verify_integrity(nombre, dim_imagen = None, RGB = None, nombre_destino = None, only = False,decript_number = None):
	print "Loading files"
	if only:
		image = open_image(nombre)
		RGB = get_RGB_list(image)
		dim_imagen = image.size
	if nombre_destino == None:
		nombre_destino = nombre
	ais_data = read_ais_head(nombre_destino.split(".")[0]+".ais")
	ais_pixels = open_ais_file(nombre_destino.split(".")[0]+".ais",ais_data,decript_number)
	print "Verifing integrity"
	print "Name: "+ str(ais_data[2] == nombre)
	print "Image resolution: "+ str(ais_data[4] == dim_imagen)
	print "Pixel per pixel verification: "+ str(ais_pixels == RGB)
	if ais_data[2] == nombre and ais_data[4] == dim_imagen and ais_pixels == RGB:
		print "Everything looks good :D"
	else:
		print "Something go wrong :c"
	return

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

def ais_main(name = None, toname = None, arguments = []):
	nombre,nombre_destino,extra_arguments = comands_arguments(arguments)

	if extra_arguments["do-nothing"]:
		print "Doing Nothing"
		exit()

	if name != None:
	 	nombre = name

	if toname != None:
	 	nombre_destino = toname

	if extra_arguments["encript"] == True:
		extra_arguments["encript"] = 211
	if extra_arguments["only-encript"]== True:
		extra_arguments["only-encript"] = 211

	if extra_arguments["only-encript"] != None:
		ais_data = read_ais_head(nombre)
		ais_pixels = open_ais_file(nombre,ais_data,extra_arguments["only-encript"])
		write_ais_file(ais_data[2], ais_pixels, ais_data[4], nombre_destino, encript_number = extra_arguments["only-encript"])
		exit()

	if extra_arguments["only-verify"]:
		if nombre and nombre_destino:
			verify_integrity(nombre,nombre_destino = nombre_destino,only = True,decript_number = extra_arguments["encript"])
		else:
			print "You have to put an name and an destiny name to verify integrity"
		exit()

	if nombre == None:
		nombre = raw_input("Filename: ")
		nombre_destino = raw_input("Destiny filename (leave blank to autoname): ")
		if nombre_destino == "":
			nombre_destino = None
	if "."+nombre.split(".")[1].lower() not in formats:
		print "The file is not an image"
		exit()

	if "."+nombre.split(".")[1].lower() != ".ais":
		imagen_cargada = open_image(nombre)
		RGB = get_RGB_list(imagen_cargada)
		if nombre_destino == None:
			write_ais_file(nombre, RGB, imagen_cargada.size,encript_number = extra_arguments["encript"])
			if extra_arguments["verify"]:
				verify_integrity(nombre,imagen_cargada.size,RGB,decript_number = extra_arguments["encript"])
		else:
			write_ais_file(nombre, RGB, imagen_cargada.size,nombre_destino = nombre_destino,encript_number = extra_arguments["encript"])
			if extra_arguments["verify"]:
				verify_integrity(nombre,imagen_cargada.size,RGB,nombre_destino,decript_number = extra_arguments["encript"])
	else:
		ais_data = read_ais_head(nombre)
		ais_pixels = open_ais_file(nombre,ais_data,extra_arguments["encript"])
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

print "Load done"

if __name__== "__main__":
	ais_main()#"test.png",arguments=["-v"])

#E.O.F End of file