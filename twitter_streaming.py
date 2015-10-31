#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import os
import json
import sys
import argparse

parser=argparse.ArgumentParser(description="TweetBot 1.0 Co-Developed by Amr El Sisy and Anmol Singh Hundal")

parser.add_argument('-o', action="store", dest='path', required=True, metavar='Output_Path', help='path to store files of streamed tweets')
parser.add_argument('-S', action="store", dest='size', type=int, default=10, metavar='Size', help='specify size of a single file in MegaBytes')
parser.add_argument('-n', action="store", dest='number', type=int, default=500, metavar='Number_of_Files', help='Specify the number of files we want to save')

parsed_args=parser.parse_args()
number=print parsed_args.number
path=print parsed_args.path
size=print parsed_args.size
sys.exit()

#VARIABLES THAT CONTAIN THE USER CREDENTIALS TO ACCESS TWITTER API
access_token = "269391427-milwXV0oyqRCIqCwGxIjzQkFb1ACABQztqJbUbK0"
access_token_secret = "pGpnbtxvOWt6yRAQwwFidJDnO67A9Jmv0gOc6NlgvkVsA"
consumer_key = "KHaVQSfjXZhOPvguDpwxOKwXO"
consumer_secret = "zoQDy3Cxoo0hEbjBdkMu3vywrVZL424JFX8i06xERj7tBabm7T"

#This will determine how many files this crawler creates
#Each file is 10 MB by default.
#When total size is 500, our crawler will create 500 files, each one of those will have the specified size.
#This will result in a total of 5 GB worth of data.
TotalNum = number # 10MB * 500 = 5GB (5GB OF DATA IS WHATS REQUIRED)
sizebytes=size*1024*1024

#first file will be called "twitter_store1.txt", second file "twitter_store2.txt", and so on, till "twitter_store500.txt"
Filenum = 1

#THIS IS A BASIC LISTENER THAT JUST PRINTS RECIEVED TWEETS TO STDOUT
class listener(StreamListener):
    def on_data(self, data):
        global Filenum #for Filenum to be defined inside function
        with open("twitter_store"+str(Filenum)+".txt", 'a') as output:
            print "Opened file"
            if(os.path.getsize("twitter_store"+str(Filenum)+".txt") < sizebytes): #10000000 is 10 MB
                output.write(data)
                #This if statement checks if file size is less than 10MB, if it is, we keep outputting to the file
            else:
                if(Filenum < TotalNum): #if file size is 10 MB we start outputting to a new file
                    Filenum = Filenum + 1
                else:
                    stream.disconnect() #when filenum = totalsize, we disconnet the streamer
                    #This will make our streamer stop streaming once we get 5 GB worth of data
        print "Closed file"

    def on_error(self, status):
        print status

if __name__ == '__main__':

    #THIS HANDLES TWITTER AUTHENTICATION AND THE CONNECTION TO TWITTER STREAMING API

    l = listener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #LOCATION OF USA = [-124.85, 24.39, -66.88, 49.38,]
    #filter tweets from the USA, and are written in English
    stream.filter(locations = [-124.85, 24.39, -66.88, 49.38,], languages=['en'])
