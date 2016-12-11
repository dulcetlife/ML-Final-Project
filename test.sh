vw -i iris.model --learning_rate=0.5 -t -p ./predictions.txt --link=logistic --compressed < verbsAndSent.vw.gz
#python3 accuracy.py indexes.txt correctVerbs.txt allVerbs.txt
