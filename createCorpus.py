import random
from random import shuffle
import time
from collections import Counter
import gzip
import io
import operator
from nltk.util import bigrams

verb_tokens = ["VVFIN", "VAFIN", "VMFIN", "VVINF", "VAINF", "VMINF", "VVIMP", "VAIMP", "VVPP", "VAPP", "VMPP", "VVIZU"]
#allVerbs = set()
#create two lists, one for training, one for testing!!!!!!
allVerbsTest = []
allVerbsTrain = []
trueVerbs = []
freqVerbsTrain = Counter()
freqVerbsTest = Counter()
upperCase = map(chr, range(65, 91))


def readData(text, format):
	if format == "train":
		#size = len(text)
		size = 200000
	else:
		#size = len(text)*0.30
		size = int(200000*0.30)
	listOfText = []
	temp = []
	sentWithEndVerb = []
	for i in text:
		temp.append(i)
	#for i in range(0,len(temp)):
	for i in range(0,size):
		#getVerbs(temp[i])
		get(temp[i],format)
		listOfText.append(temp[i][0:-6])
	#print(listOfText)
	for i in listOfText:
		end = i[-5:]
		if end in verb_tokens:
			sentWithEndVerb.append(i)
	return sentWithEndVerb	

def get(sent,format):
	temp = sent.split()
	temp2 = []
	for i in temp:
		t = i.split("_")
		temp2.append(t)
	for i in range(0,len(temp2)):
		if temp2[i][1] in verb_tokens:
			if format == "train":
				allVerbsTrain.append(temp2[i][0])
			else:
				allVerbsTest.append(temp2[i][0])


def outputFile(text, testVerbs):
	newFile = io.BufferedWriter(gzip.open("verbsAndSent.vw.gz", "w"))
	for i in text:
		verb = i.rsplit(" ", 1)[-1]
		trueVerbs.append(verb)
		rest = i.rsplit(" ", 1)[0]
		bi = list(bigrams(rest.split()))
		for j in testVerbs:
		#for j in allVerbsTest:
			biVerb = list(bigrams(j))
			newFile.write("1 |words ")
			newFile.write(rest)
			newFile.write(" ")
			newFile.write(' '.join(''.join(elems) for elems in bi))
			newFile.write(" |verbs ")
			newFile.write(j)
			#newFile.write(" ")
			#newFile.write(' '.join(''.join(x) for x in biVerb))
			newFile.write("\n")

def cleanUp(sent):
	newSent = list(sent)
	
	for i in range(0,len(newSent)):
		if newSent[i] == "_":
			for j in range(1,8):
				try:
					if(newSent[i+j] in upperCase):
						newSent[i+j] = ""
					else:
						break
				except Exception:
					break
								
	removeChar = ["#", "_", "$,", "$", "(", ")", "/", '"', "-", "*", ":"]
	#removeChar = ["#", "_", "$,", "$"]
	for i in range(0,len(newSent)):
		if newSent[i] in removeChar:
			newSent[i] = ""
	
	for i in range(0, len(newSent)):
		#if newSent[i] == "," and newSent[i+3] == ",":
		if newSent[i] == ",":
			newSent[i] = ""
			#newSent[i+4] = ""
		
	clean = ''.join(newSent)

	return clean

def getFreq(allVerbsTrain):
	for i in allVerbsTrain:
		freqVerbsTrain[i] +=1
	#for i in allVerbsTest:
		#freqVerbsTest[i] +=1
	#lenTest = len(freqVerbsTest)
	#lenTrain = len(freqVerbsTrain)
	#dict with frequency of the top 30% most common verbs from the testing data
	#verbsTest = dict(freqVerbsTest.most_common(int(lenTest*0.30)))
	#dict with frequencw toy of the top 30% most common verbs from the training data
	verbsTrain = dict(freqVerbsTrain.most_common(50))
	#list of all the verbs from the training data
	trainVerbs =  verbsTrain.keys()
	#list of all the verbs from the testing data
	#testVerbs = verbsTest.keys()
	#return(verbsTrain,verbsTest, trainVerbs, testVerbs)
	return(trainVerbs)

def convertToVW(text, format, verbsTrain):
	sortedVerbs = sorted(verbsTrain.items(), key = lambda i: i[1], reverse = True)
	sort = []
	for i in range(0,len(sortedVerbs)):
		sort.append(sortedVerbs[i][0])
	print(sort)
	if format == "train":
		newFile = open("verbTraining.vw", "w")
	else:
		newFile = open("verbTesting.vw", "w")
	for i in text:
		lastWord = i.rsplit(" ", 1)[-1]
		randVerb = lastWord
		'''verbFreq = float(freqVerbsTrain[lastWord])/float(len(freqVerbsTrain))
		for j in freqVerbsTrain:
			freq = freqVerbsTrain[j]/float(len(freqVerbsTrain))
			if freq - freq*0.05 <= verbFreq <= freq + freq*0.05:
				if j == lastWord:
					continue
				else:
					randVerb = j
					break'''
		
		if lastWord not in sort:
			continue
		verbRank = sort.index(lastWord)
		for j in sort:
			rank = sort.index(j)
			#print(freq)
			#USE RANK
			if abs(rank - 10) <= verbRank <= rank + 10:
				if j == lastWord:
					continue
				else:
					randVerb = j
					break

		#if randVerb == lastWord:
			#continue
			#randVerb = random.choice(verbsTrain.keys())
		rest = i.rsplit(" ", 1)[0]
		bi = list(bigrams(rest.split()))
		biVerb = list(bigrams(lastWord))
		negBiVerb = list(bigrams(randVerb))
		
		newFile.write("1 |words ")
		newFile.write(rest)
		newFile.write(" ")
		newFile.write(' '.join(''.join(elems) for elems in bi))
		newFile.write(" |verbs ")
		newFile.write(lastWord)
		#newFile.write(" ")
		#newFile.write(' '.join(''.join(x) for x in biVerb))
		newFile.write("\n")
		newFile.write("-1 |words ")
		newFile.write(rest)
		newFile.write(" ")
		newFile.write(' '.join(''.join(elems) for elems in bi))
		newFile.write(" |verbs ")
		newFile.write(randVerb)
		#newFile.write(" ")
		#newFile.write(' '.join(''.join(y) for y in negBiVerb))
		newFile.write("\n")


def writeToFile(testVerbs):
	correctVerbs = open("correctVerbs.txt", "w")
	allTheVerbs = open("allVerbs.txt", "w")
	for i in trueVerbs:
		correctVerbs.write(str(i))
		correctVerbs.write("\n")
	for j in testVerbs:
		allTheVerbs.write(str(j))
		allTheVerbs.write("\n")
	metaData = open("meta.txt", "w")
	metaData.write(str(len(testVerbs)))

def createNewTrainCorpus(cleanedSentTrain, trainVerbs):
	trainCorpus = open("training.txt", "w")
	for i in cleanedSentTrain:
		lastWord = i.rsplit(" ", 1)[-1]
		if lastWord in trainVerbs:
			trainCorpus.write(i)
			trainCorpus.write("\n")

def createNewTestCorpus(cleanedSentTest, trainVerbs):
	testCorpus = open("testing.txt", "w")
	for i in cleanedSentTest:
		lastWord = i.rsplit(" ", 1)[-1]
		if lastWord in trainVerbs:
			testCorpus.write(i)
			testCorpus.write("\n")


def main():
	start_time = time.time()
	trainData = open("1M-tagged.txt", "r")
	testData = open("1M-tagged_test.txt", "r")
	verbSentTrain = readData(trainData, "train")
	verbSentTest = readData(testData, "test")
	#verbsTrain, verbsTest, trainVerbs, testVerbs = getFreq(allVerbsTrain, allVerbsTest)
	trainVerbs = getFreq(allVerbsTrain)
	cleanedSentTrain = []
	cleanedSentTest = []
	for i in verbSentTrain:
		cleanedSentTrain.append(cleanUp(i))
	for j in verbSentTest:
		cleanedSentTest.append(cleanUp(j))
	createNewTrainCorpus(cleanedSentTrain, trainVerbs)
	createNewTestCorpus(cleanedSentTest, trainVerbs)
	#outputFile(cleanedSentTest, testVerbs)
	#convertToVW(cleanedSentTrain, "train", verbsTrain)
	#writeToFile(allVerbsTest)
	#writeToFile(testVerbs)
	#print(len(trainVerbs))
	#print(len(testVerbs))
	print("--- %s seconds ---" % (time.time() - start_time))
	#print(len(cleanedSentTest)*len(allVerbsTest))
	#print(len(allVerbsTest))
	

	
	

if __name__ == '__main__':
	main()