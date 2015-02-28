## Alf Image System
##
## History:
## "1.indev"
##

version = "1.indev"
print "Loading Alf Image System v"+str(version)+" ..."
import sys, os, Image, ais_commons


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

def ais_main_1.x():
	image = ais_commons.open_image("test.png")
	RGB = ais_commons.get_RGB_list(image)
	print get_color_pixels(RGB)
	return

#E.O.F End of file