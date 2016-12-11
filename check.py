

def checkFile(fileName):
	new = []
	with open("meta.txt") as g:
		temp = g.readlines()
	rate = int(temp[0])
	with open(fileName) as f:
		predictions = f.readlines()
	for i in predictions:
		new.append(i.rstrip("\n"))
	indexes = open("indexes.txt", "w")
	for i in range(0,len(new),rate):
		#print(count)
		stop = i + rate
		sent = new[i:stop]
		maxx = max(sent)
		index = sent.index(maxx)
		indexes.write(str(index))
		indexes.write("\n")

def main():
	fileName = "predictions.txt"
	checkFile(fileName)

if __name__ == '__main__':
	main()