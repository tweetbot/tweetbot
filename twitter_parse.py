import json
import pandas as pd
import re
import os

tweets_data_path = "/Users/aelsi001/desktop/twitter_store.txt"
path = "/Users/aelsi001/desktop/"

with open(tweets_data_path, "r") as myfile:
	text = myfile.read()

#urls = re.findall('inspired', text)
#print urls
