#calculates the accuracy of the predicted values from Vowpal Wabbit
from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
import itertools
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import sys
predictRaw = []

def getFile():
	file_name_indexes = sys.argv[1]
	with open(file_name_indexes) as f:
		indexes = f.readlines()
	for i in range(0,len(indexes)):
		indexes[i] = int(indexes[i])
	
	file_name_correct = sys.argv[2]
	with open(file_name_correct) as g:
		correctVerbs = g.readlines()

	file_name_allVerbs = sys.argv[3]
	with open(file_name_allVerbs) as h:
		allVerbs = h.readlines()

	return indexes, correctVerbs, allVerbs
	
def predict(indexes, allVerbs):
	predictedVerbs = []
	for i in indexes:
		predictedVerbs.append(allVerbs[i])
	return predictedVerbs


def getAccuracy(correctVerbs, predictedVerbs):
	correct = 0.0
	for i in range(len(correctVerbs)):
		try:
			if (correctVerbs[i]) == (predictedVerbs[i]):
				correct += 1
		except Exception:
			continue		
	return (correct/float(len(correctVerbs))) * 100.0

def confusionMatrix(cm, correctVerbs,predictedVerbs, allVerbs):
	#[x.encode('utf-8') for x in correctVerbs]
	plt.imshow(cm, interpolation = "nearest", cmap = plt.cm.Blues)
	plt.title("Confusion Matrix")
	plt.colorbar()
	tick_marks = np.arange(len(allVerbs))
	plt.xticks(tick_marks, allVerbs, rotation = 45)
	plt.yticks(tick_marks, allVerbs)
	print(cm)
	thresh = cm.max()/2
	for i,j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
		plt.text(j, i, cm[i,j], horizontalalignment = "center", color = "white" if cm[i,j] > thresh else "black")
	#plt.tight_layout()
	plt.ylabel("True Label")
	plt.xlabel("Predicted Label")



def main():
	indexes, correctVerbs, allVerbs = getFile()
	predictedVerbs = predict(indexes, allVerbs)
	accuracy = getAccuracy(correctVerbs, predictedVerbs)
	#print(len(correctVerbs))
	#print(len(predictedVerbs))
	print("Accuracy of Vowpal Wabbit is", accuracy, "%")
	cm = confusion_matrix(correctVerbs, predictedVerbs)
	np.set_printoptions(precision = 2)
	#plt.figure()
	#confusionMatrix(cm, correctVerbs, predictedVerbs, allVerbs)
	#plt.show()

	

if __name__ == '__main__':
	main()