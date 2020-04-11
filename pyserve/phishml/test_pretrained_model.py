# https://github.com/faizann24/phishytics-machine-learning-for-phishing

# Basic libraries
import os
import io
import sys
import math
import time
import random
import requests
import collections
import numpy as np
from os import walk
import pandas as pd
from joblib import dump, load
from langdetect import detect
from tokenizers import ByteLevelBPETokenizer

"""
How to run:
python3 test_pretrained_model.py --tokenizer_folder pretrained_models --threshold 0.5 --model_dir pretrained_models --website_to_test https://www.google.com
"""

def runPhishCheck(website):
	tokenizerFolder = "pretrained_models"
	savedModelDirectory = "pretrained_models"
	threshold = 0.5

	# Loading files
	# Load tokenization files
	tokenizer = ByteLevelBPETokenizer(
		tokenizerFolder + "/pretrained_Tokenizer-10000.tok-vocab.json",
		tokenizerFolder + "/pretrained_Tokenizer-10000.tok-merges.txt",
	)
	tokenizerVocabSize = tokenizer.get_vocab_size()

	# Load saved model
	model = load(savedModelDirectory + "/pretrained-phishytics-model.joblib")

	# Load document frequency dictionary
	docDict = np.load(savedModelDirectory + "/document-frequency-dictionary.npy", allow_pickle=True).item()

	# Testing
	try:
		request = requests.get(website)
		webpageHtml = str(request.text)
		webpageHtml = webpageHtml.replace("\n", " ")

		# Convert text into feature vector
		output = tokenizer.encode(webpageHtml)
		outputDict = collections.Counter(output.ids)
	except Exception as e:
		print("**** Error loading the website ****")
		print(e)
		exit()

	# Apply tfidf weighting
	totalFilesUnderConsideration = 18500 # total number of documents/html files in our training data
	array = [0] * tokenizerVocabSize
	for item in outputDict:
		if len(docDict[item]) > 0:
			array[item] = (outputDict[item]) * (math.log10( totalFilesUnderConsideration / len(docDict[item] )))

	# Getting predictions
	predictionProbability = model.predict_proba([array])[0][1]
	# print("\n****************************\n--> Probability that the website is phishing: %.2f" % (predictionProbability * 100))

	# Default is not phishing 
	prediction = False
	if predictionProbability > threshold:
		prediction = True
	print(prediction)
	return prediction
	# print("--> Based on your threshold of %.2f, this website is +++'%s'+++" % (threshold, prediction))
	# print("****************************")

# Only for running the script directly like cli
if __name__ == "__main__":
    # execute only if run as a script
    website = sys.argv[1]
    runPhishCheck(website)