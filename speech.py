#!/usr/bin/python

import sys
import urllib2
import os
import json
import subprocess as sp

url = "https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=en-US"
fileName = str(sys.argv[1])
fileExtension = os.path.splitext(fileName)[1]
converted = False

if fileExtension != ".flac":
	fnull = open(os.devnull, 'w')
	sp.call("pacpl --overwrite -t flac " + fileName, shell = True, stdout = fnull, stderr = fnull)
	fnull.close()
	fileName = os.path.splitext(fileName)[0] + '.flac'
	converted = True

try:
	binary_audio = open(fileName, 'rb')
except:
	print "Failed to get binary data."

size_of_audio = os.path.getsize(fileName)

if converted:
	os.remove(fileName)

request = urllib2.Request(url)
request.add_header('Content-type','audio/x-flac; rate=16000')
request.add_header('Content-length', str(size_of_audio))
request.add_data(binary_audio)

try:
	response = urllib2.urlopen(request)
except urllib2.URLError, e:
	print "Unable to connect"
except urllib2.HTTPError, e:
	print "Oops, bad request"

content = response.read()

data = json.loads(content)

print data["hypotheses"][0]["utterance"]

