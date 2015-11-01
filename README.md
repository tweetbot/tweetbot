Tweetbot - Multithreaded Tweet Catcher
===========================================

This is Tweetbot, a multithreaded Twitter Informational Retrival System. 

Feature
-------
-	Multithread Support. The API supports only one streaming thread, but we can have multiple parsing threads.
-  Can Specify number of parser threads using -t flag.
-  Crawls any webpages in the tweet and stores the title of the page along with the tweet.
-  Respects Robot ethics of webpages.

Installation
------------
```bash
sudo apt-get install pip
sudo pip install --upgrade pip
sudo pip install virtualenv

#Create a new virtual environment
virtualenv tweetbot_env

#This will create a python venv in your current folder
#To use the virtual environment, first we need to activate it
source tweetbot_env/bin/activate

#install dependencies
pip isntall -r requirements.txt

#run tweetbot with help flag to learn more
python tweetbot.py -h

#to deactivate the virtualenv
deactivate
```
##MIT License