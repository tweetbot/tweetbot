#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from threading import Thread
from threading import current_thread
from Queue import Queue
import threading
import itertools
import os
import json
import sys
import argparse
import time
import signal

#VARIABLES THAT CONTAIN THE USER CREDENTIALS TO ACCESS TWITTER API
access_token = "269391427-milwXV0oyqRCIqCwGxIjzQkFb1ACABQztqJbUbK0"
access_token_secret = "pGpnbtxvOWt6yRAQwwFidJDnO67A9Jmv0gOc6NlgvkVsA"
consumer_key = "KHaVQSfjXZhOPvguDpwxOKwXO"
consumer_secret = "zoQDy3Cxoo0hEbjBdkMu3vywrVZL424JFX8i06xERj7tBabm7T"

#Arguments Parsing
parser=argparse.ArgumentParser(description="TweetBot 1.0 Co-Developed by Amr El Sisy and Anmol Singh Hundal")

parser.add_argument('-o', action="store", dest='path', required=True, metavar='Output_Path', help='path to store files of streamed tweets')
parser.add_argument('-S', action="store", dest='size', type=int, default=10, metavar='Filesize', help='specify size of a single file in MegaBytes')
parser.add_argument('-n', action="store", dest='number', type=int, default=500, metavar='Number_of_Files', help='Specify the number of files we want to save')
parser.add_argument('-t','--threads', action="store", dest='threadcount', type=int, default=1, choices=xrange(2,5), metavar='Number of threads', help='Specify the number of threads you want to run')

parsed_args=parser.parse_args()
NUMBEROFFILES=parsed_args.number
PATH=parsed_args.path
FILESIZE=parsed_args.size
PWORKERS=1

#Error chceking for filepath
filepath=''
if PATH=='':
    print "Empty path specified"
    exit()
elif PATH[-1]=='/':
    filepath=PATH
else:
    filepath=PATH+'/'


#File Size in bytes
FILESIZEBYTES=FILESIZE*1024*1024

#Listener that catches tweets and puts them on raw tweets list
class listener(StreamListener):
    def on_data(self, data):
        if terminator:
            streamobj.disconnect()

        raw_tweets.put(data,True)
        #print "Put on Rawqueue. RawSize", raw_tweets.qsize()

    def on_error(self, status):
        if terminator:
            tloc.stream.disconnect()
        tloc.stream.disconnect()
        print status

#Thread class that runs listener
class StreamingWorker(Thread):
    def __init__(self, auth, listener):
        Thread.__init__(self)
        self.auth=auth
        self.listener=listener

    def run(self):
        global streamobj
        streamobj = Stream(self.auth, self.listener)

        #LOCATION OF USA = [-124.85, 24.39, -66.88, 49.38,] filter tweets from the USA, and are written in English
        streamobj.filter(locations = [-124.85, 24.39, -66.88, 49.38,], languages=['en'])
        return

#Thread class that runs parser
class ParsingWorker(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global terminator
        #print "started parsing thead", current_thread().getName()
        while 1:
            if terminator:
                break
            curtweet=raw_tweets.get(True)
            #print "Got an item from raw_tweets", current_thread().getName()

            #Do some processing here

            processed_tweets.put(curtweet,True)
            #print "Put on processed queue. ProcessedSize", processed_tweets.qsize()

#Thread class that saves tweets from processed queue into a file
class SavingWorker(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        #FIXME
        #do path and file verification here.
        global filecounter
        global terminator
        #print "Started saving thead", current_thread().getName()

        while 1:
            if terminator:
                break
            curtweet=processed_tweets.get(True)

            #This if statement checks if file size is less than 10MB, if it is, we keep outputting to the file
            if(os.path.exists(filepath+"twitter_store"+str(filecounter)+".txt")):
                if(os.path.getsize(filepath+"twitter_store"+str(filecounter)+".txt") >= FILESIZEBYTES): #10000000 is 10 MB
                    filecounter+=1
            if filecounter>NUMBEROFFILES:
                terminator=True

            with open(filepath+"twitter_store"+str(filecounter)+".txt", 'a') as output:
                output.write(curtweet)


#For Streaming
l = listener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Global File Counter
filecounter=0

#Global Tweets Lists
raw_tweets=Queue(10)
processed_tweets=Queue(10)

#thread local storage
tloc=threading.local()

#global terminate status
terminator=False

#Signal Handler for SIGINT (Ctrl-C)
def signal_handler(signal, frame):
    if current_thread().getName()=='MainThread':
        print("\nCleaning up..")
    global terminator
    terminator=True
    while threading.active_count() > 1:
        time.sleep(0.1)
    if current_thread().getName()=='MainThread':
        print "Exiting."
    sys.exit()

signal.signal(signal.SIGINT,signal_handler)

#Start the streamer thread
streamer=StreamingWorker(auth,l)
streamer.setDaemon(True)
streamer.start()

#start processor threads
for y in range(PWORKERS):
    pworker=ParsingWorker()
    pworker.setDaemon(True)
    pworker.start()

#start filesaver thread
filesaver=SavingWorker()
filesaver.setDaemon(True)
filesaver.start()

while threading.active_count() > 1:
        time.sleep(0.1)
