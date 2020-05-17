#!/bin/bash
# MALLET_LOCATION='../../Mallet-master' #change to your own Mallet location,
# relative to container path. Since we provision the mallet executable, you can just point this location to that exec.
export MALLET_EXEC='mallet'

# prepare training/testing documents
dataset='cord-19'
mallet import-file --input ./data/epoch_mallet_inputs/train/train.txt \
--output ./data/$dataset/train.mallet \
--label-as-features --keep-sequence --remove-stopwords --line-regex '([^\t]+)\t([^\t]+)\t(.*)'
#
mallet import-file --input ./data/epoch_mallet_inputs/test/test.txt \
--output ./data/$dataset/test.mallet \
--label-as-features --keep-sequence --remove-stopwords --line-regex '([^\t]+)\t([^\t]+)\t(.*)'
#
# # prepare word features
#
java -cp /opt/MetaLDA/target/metalda-0.1-jar-with-dependencies.jar topicmodels.BinariseWordEmbeddings \
--train-docs ./data/$dataset/train.mallet \
--test-docs ./data/$dataset/test.mallet \
--input ./data/$dataset/raw_embeddings.txt \
--output ./data/$dataset/binary_embeddings.txt
#
# echo 'binarising word embeddings finished ...'
#
# train MetaLDA

topics=30

alphamethod=0

betamethod=0

savedir=./save && mkdir -p $savedir;

#java8 if using locally... Calvin was having issues running this with newest java
java -Xmx8g -cp /opt/MetaLDA/target/metalda-0.1-jar-with-dependencies.jar topicmodels.MetaLDATrain \
--train-docs ../data/$dataset/train.mallet \
--num-topics $topics \
--word-features ../data/$dataset/binary_embeddings.txt \
--save-folder $savedir \
--sample-alpha-method $alphamethod \
--sample-beta-method $betamethod


# inference without unseen words
#
# java -Xmx4g -cp ../target/metalda-0.1-jar-with-dependencies.jar topicmodels.MetaLDAInfer \
# --test-docs ../data/$dataset/test_doc.mallet \
# --save-folder $savedir \
# --compute-perplexity true;
#
# echo 'inference without unseen words finished ...'

# inference with unseen words
#
# java8 -Xmx4g -cp ../target/metalda-0.1-jar-with-dependencies.jar topicmodels.MetaLDAInferUnseen \
# --test-docs ../data/$dataset/test_doc.mallet \
# --save-folder $savedir \
# --compute-perplexity true \
# --word-features ../data/$dataset/binary_embeddings.txt
