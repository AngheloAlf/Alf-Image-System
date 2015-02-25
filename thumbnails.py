from PIL import Image
import glob, os

size = 128, 128
print size
# for infile in glob.glob("*.jpg"):
#     file, ext = os.path.splitext(infile)
#     im = Image.open(infile)
#     im.thumbnail(size, Image.ANTIALIAS)
#     im.save(file + ".thumbnail.jpg", "JPEG")

im = Image.new("RGB",size,"white")
print im
im.save("bla" + ".thumbnail.jpg", "JPEG")