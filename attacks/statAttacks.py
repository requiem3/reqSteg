#arg1 = 'chi' (only method for now, arg2=image

from PIL import Image
import sys

def chiSquared(c):
	carrier=Image.open(c)
	carrier=carrier.convert("RGB")
	testStatistic=0
	sumRed=0
	sumBlue=0
	sumGreen=0
	sumTotal=0
	counter=0
	width, height = carrier.size
	freedom=(width-1)*(height-1)
	
	matrix = [[0 for x in range(3)] for y in range(height*width)]
	for x in range(width): #assign all RGB values to matrix ((256,256,256),(256,256,256),...)
		for y in range(height):
			matrix[counter][0]=carrier.getpixel((x,y))[0]
			matrix[counter][1]=carrier.getpixel((x,y))[1]
			matrix[counter][2]=carrier.getpixel((x,y))[2]
			counter+=1	

	nMatrix=[x+[sum(x)] for x in matrix] # new matrix with fourth value of tuple being sum of previous 3, for chi-squared test

	for x in nMatrix: #finish the chi-squared table
		sumRed+=x[0]	
		sumGreen+=x[1]
		sumBlue+=x[2]
		sumTotal+=x[3]

	for x in range(len(nMatrix)):
		#print nMatrix[x][3]
		testStatistic+=calcExpected(nMatrix[x][0],nMatrix[x][3],sumRed,sumTotal)
		testStatistic+=calcExpected(nMatrix[x][1],nMatrix[x][3],sumGreen,sumTotal)
		testStatistic+=calcExpected(nMatrix[x][2],nMatrix[x][3],sumBlue,sumTotal)

	print testStatistic #if testStatistic > freedom then something be amiss (possibly)
	
	
def calcExpected(cVal,totalAllC,totalC,totalAll):
	expected=totalAllC*(float(totalC)/totalAll)

	return(pow(cVal-expected,2)/expected)
	
if __name__ == "__main__": 
	if sys.argv[1] == "chi":
		chiSquared(sys.argv[2])
	else:
		print "no valid method for arg1"
