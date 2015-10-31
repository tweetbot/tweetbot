#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from threading import Thread
from threading import current_thread
import threading
from Queue import Queue
import itertools
import os
import json
import sys
import argparse

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
parser.add_argument('-t','--threads', action="store", dest='threadcount', type=int, default=1, metavar='Number of threads', help='Specify the number of threads you want to run')

parsed_args=parser.parse_args()
NUMBEROFFILES=parsed_args.number
PATH=parsed_args.path
FILESIZE=parsed_args.size
STREAMERS=parsed_args.threadcount

TotalNum = NUMBEROFFILES
FILESIZEBYTES=FILESIZE*1024*1024

#THIS IS A BASIC LISTENER THAT JUST PRINTS RECIEVED TWEETS TO STDOUT
class listener(StreamListener):
    def on_data(self, data):
        global tloc
        print current_thread(), "Caught a tweet"

        #do some processing here

        with open("twitter_store"+str(tloc.fn)+".txt", 'a') as output:
            if(os.path.getsize("twitter_store"+str(tloc.fn)+".txt") < FILESIZEBYTES): #10000000 is 10 MB
                output.write(data)
                #This if statement checks if file size is less than 10MB, if it is, we keep outputting to the file
            else:
                if(tloc.fn < TotalNum): #if file size is 10 MB we start outputting to a new file
                    global filecounter
                    tloc.fn=filecounter.next()
                else:
                    stream.disconnect() #when filenum = totalsize, we disconnet the streamer
                    #This will make our streamer stop streaming once we get 5 GB worth of data

    def on_error(self, status):
        print status

class StreamingWorker(Thread):
    def __init__(self, auth, listener):
        Thread.__init__(self)
        self.auth=auth
        self.listener=listener

    def run(self):
        #Handles thread local storage for filenum
        global tloc
        tloc.fn=filecounter.next()

        #Handles streaming
        stream = Stream(self.auth, self.listener)
        #LOCATION OF USA = [-124.85, 24.39, -66.88, 49.38,] filter tweets from the USA, and are written in English
        stream.filter(locations = [-124.85, 24.39, -66.88, 49.38,], languages=['en'])



#For Streaming
l = listener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#File Counter
filecounter=itertools.count()

#thread local storage
tloc=threading.local()

for x in range(STREAMERS):
    streamer=StreamingWorker(auth,l)
    streamer.start()
