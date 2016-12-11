rm predictions.txt
rm iris.model
gshuf verbTraining.vw > verbTrainingShuffled.vw
vw -f iris.model --passes=2 --cache_file=iris.cache --kill_cache -q vv -q wv -q cv --loss_function=logistic --l2 0.003 < verbTrainingShuffled.vw