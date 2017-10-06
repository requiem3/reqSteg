#terrible encoding for red pixels only to test stat attacks

#Encodes message into only the red RGB of a pixel at a set width + height, then shows how it decodes
#special characters dont work
#some pixels contain 7 bits not 8 which causes problems sometimes.????? 

from PIL import Image, ImageDraw
import binascii

carrier = Image.open("stego.png")
carrier = carrier.convert("RGB")
draw = ImageDraw.Draw(carrier)
message="does it detect even small messages?"

maxW = 200
maxH = 200
widthC = 0
heightC = 0

def swapBits(swapVal):
	global widthC, heightC, maxW, maxH, carrier
	if widthC < maxW:
		pixel = carrier.getpixel((widthC,heightC))
		binRGB = bin(pixel[0])[2:9] + str(swapVal)
		carrier.putpixel((widthC,heightC),int(binRGB,2))
		pixel = carrier.getpixel((widthC,heightC))
		widthC += 1
	elif heightC < maxH:
		heightC += 1
		widthC = 0
		pixel = carrier.getpixel((widthC,heightC))
		binRGB = bin(pixel[0])[2:9] + str(swapVal)
		carrier.putpixel((widthC,heightC),int(binRGB,2))
		widthC += 1
	else:
		print 'too wordy, message doesnt fit'	

message = message.replace(' ','')
for c in range(len(message)):
	for x in bin(ord(message[c])).replace('b',''): 
		swapBits(x)
carrier.save("stegoNew.png")

counter=0
stg=''
widthC = 0
heightC = 0
final=''
def getMessage():
	global widthC, heightC, maxW, maxH,counter,stg,carrier,final
	while heightC < 10:
		while widthC < 200:
			pixel = carrier.getpixel((widthC,heightC))
			if counter == 8:
				final += chr(int(stg,base=2))
				stg = ''
				counter = 0
			stg += str(bin(pixel[0])[9])
			counter += 1
			widthC += 1
		heightC += 1
		widthC = 0
	
getMessage()
print final
