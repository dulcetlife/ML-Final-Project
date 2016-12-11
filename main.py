import random
from random import shuffle
import time
from collections import Counter
import gzip
import io
import operator
from nltk.util import bigrams
import re
from textblob_de import TextBlobDE as TextBlob
import sys  # import sys package, if not already imported
reload(sys)
sys.setdefaultencoding('utf-8')

verb_tokens = ["VB", "VBZ", "VBP", "VBD", "VBN"]
verbsTrain = []
verbsTest = []
allVerbs = set()
trueVerbs = []
freqVerbsTrain = Counter()
freqVerbsTest = Counter()

def getData():
	trainFile = open("training.txt", "r")
	testFile = open("testing.txt", "r")
	train = []
	test = []
	for i in trainFile:
		train.append(i)
	for i in testFile:
		test.append(i)	
	trainData = [line.rstrip() for line in train]
	testData = [line.rstrip() for line in test]
	return(trainData,testData)

def getVerbsAndFreq(trainData, testData):
	for i in testData:
		verb = i.rsplit(" ", 1)[-1]
		verbsTest.append(verb)
		allVerbs.add(verb)

	for i in trainData:
		verb = i.rsplit(" ", 1)[-1]
		verbsTrain.append(verb)

	for i in verbsTrain:
		freqVerbsTrain[i] +=1

	for i in verbsTest:
		freqVerbsTest[i] +=1

def outputFile(testData):
	newFile = io.BufferedWriter(gzip.open("verbsAndSent.vw.gz", "w"))
	for i in testData:
		#i = i.encode('utf-8')
		#i = i.decode('utf-8')
		blob = TextBlob(i)
		cases = []
		for j in blob.tags:
			j = list(j)
			if j[1] in verb_tokens:
				continue
			if j[1] == "NN":
				j[1] = "1"
			elif j[1] == "NNS":
				j[1] = "2"
			elif j[1] == "NNP":
				j[1] = "3"
			elif j[1] == "NNPS":
				j[1] = "4"
			elif j[1] == "PRP":
				j[1] = "5"
			elif j[1] == "PRP$":
				j[1] = "6"
			else:
				continue
			j = tuple(j)
			cases.append(j)
		#print(cases)
		#print(blob.tags[0])
		verb = i.rsplit(" ", 1)[-1]
		trueVerbs.append(verb)
		rest = i.rsplit(" ", 1)[0]
		bi = list(bigrams(rest.split()))
		for j in allVerbs:
		#for j in allVerbsTest:
			biVerb = list(bigrams(j))
			newFile.write("1 |words ")
			newFile.write(rest)
			newFile.write(" ")
			newFile.write(' '.join(''.join(elems) for elems in bi))
			newFile.write(" |cases ")
			newFile.write(' '.join(' '.join(x) for x in cases))
			newFile.write(" |verbs ")
			newFile.write(j)
			newFile.write(" ")
			newFile.write(' '.join(''.join(x) for x in biVerb))
			newFile.write("\n")

def convertToVW(text, freqVerbsTrain):
	sortedVerbs = sorted(freqVerbsTrain.items(), key = lambda i: i[1], reverse = True)
	sort = []
	for k in range(0,len(sortedVerbs)):
		sort.append(sortedVerbs[k][0])
	newFile = open("verbTraining.vw", "w")	
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
					break
		
		if lastWord not in sort:
			continue
		'''
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
			#randVerb = random.choice(allVerbs)
		rest = i.rsplit(" ", 1)[0]
		bi = list(bigrams(rest.split()))
		biVerb = list(bigrams(lastWord))
		negBiVerb = list(bigrams(randVerb))
		blob = TextBlob(i)
		cases = []
		d = 0
		try:
			for n in blob.tags:
				n = list(n)
				if n[1] in verb_tokens:
					continue
				if n[1] == "NN":
					n[1] = "1"
				elif n[1] == "NNS":
					n[1] = "2"
				elif n[1] == "NNP":
					n[1] = "3"
				elif n[1] == "NNPS":
					n[1] = "4"
				elif n[1] == "PRP":
					n[1] = "5"
				elif n[1] == "PRP$":
					n[1] = "6"
				else:
					continue
				n = tuple(n)
				cases.append(n)
		except Exception:
			d +=1
			continue	
		newFile.write("1 |words ")
		newFile.write(rest)
		newFile.write(" ")
		newFile.write(' '.join(''.join(elems) for elems in bi))
		newFile.write(" |cases ")
		newFile.write(' '.join(':'.join(x) for x in cases))
		newFile.write(" |verbs ")
		newFile.write(lastWord)
		newFile.write(" ")
		newFile.write(' '.join(''.join(x) for x in biVerb))
		newFile.write("\n")
		newFile.write("-1 |words ")
		newFile.write(rest)
		newFile.write(" ")
		newFile.write(' '.join(''.join(elems) for elems in bi))
		newFile.write(" |cases ")
		newFile.write(' '.join(':'.join(x) for x in cases))
		newFile.write(" |verbs ")
		newFile.write(randVerb)
		newFile.write(" ")
		newFile.write(' '.join(''.join(y) for y in negBiVerb))
		newFile.write("\n")
	print(d)
def writeToFile():
	correctVerbs = open("correctVerbs.txt", "w")
	allTheVerbs = open("allVerbs.txt", "w")
	for i in trueVerbs:
		correctVerbs.write(str(i))
		correctVerbs.write("\n")
	for j in allVerbs:
		allTheVerbs.write(str(j))
		allTheVerbs.write("\n")
	metaData = open("meta.txt", "w")
	metaData.write(str(len(allVerbs)))

def sentenceLength(trainData, testData):
	sentLengthTrain = []
	sentLengthTest = []
	for i in trainData:
		length = len(i)
		sentLengthTrain.append(length)
	for i in testData:
		length = len(i)
		sentLengthTest.append(length)

def main():
	start_time = time.time()
	trainData, testData = getData()
	getVerbsAndFreq(trainData, testData)
	outputFile(testData)
	convertToVW(trainData, freqVerbsTrain)
	writeToFile()
	#sentenceLength(trainData, testData)
	print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
	main()
