import sys
import os
import re
import tweepy
import json
from tweepy import OAuthHandler
from textblob import TextBlob
from twitter_client import get_twitter_auth
from twitter_client import get_twitter_client
from collections import Counter
from operator import itemgetter
import networkx as nx
from decimal import *
import io
#import matplotlib.pyplot as plot

api = get_twitter_client()

''' Get the tweets'''


def remove_special_chars(tweet):
	'''
	This function uses simple regular expressions statements 
	to remove links and special characters
	'''
	return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z\t])|(\w+:\/\/\S+)", " ", tweet).split())

def calculate_sentiment(tweet):
	'''
	This function uses Textblob to determine a tweet's sentiment
	'''
	expression = TextBlob(remove_special_chars(tweet))
	print (expression)
	print ("Polarity: " + str(expression.polarity) + "\nSubjectivity: "+ str(expression.subjectivity))

	if expression.sentiment.polarity > 0:
		return 'positive'
	elif expression.sentiment.polarity == 0:
		return 'neutral'
	else: 
		return 'negative'
def calculate_attention(tweet):
	'''
	This function factors in the number of retweets, likes and replies
	'''
	#no_of_likes = tweet['favorite_count'] #Not available in through the API
	no_of_retweets = tweet['retweet_count']
	#original_tweet_id = tweet['in_reply_to_status_id_str']
	#original_author_id = tweet['in_reply_to_user_id_str']
	follower_count = tweet['user']['followers_count']
	print ("No. of likes: " + str(no_of_likes) + " No. of retweets: " + str(no_of_retweets))
	if follower_count != 0:
		#return (float(no_of_likes) + float(no_of_retweets) + float(follower_count))/float(follower_count)
		return (float(no_of_retweets) + float(follower_count))/float(follower_count)
	else:
		return no_of_retweets # + no_of_likes

if __name__ == '__main__':
	arg = sys.argv[1]
	auth = api

	dirname = "users/{}".format(arg)
	sentimentdir = "users/{}/sentiment/".format(arg)
	fname1 = "users/{}/sentiment/sentiment_score.jsonl".format(arg)
	face_rating_file = "face_ratings.txt"

	try:
		os.makedirs(dirname, mode=0o755, exist_ok=True)
		os.makedirs(sentimentdir, mode=0o755, exist_ok=True)
	except OSError:
		print("Directory {} already exists". format(dirname))
		pass
	except Exception as e:
		print("Error while creating directory {}".format(dirname))
		print("Error while creating directory {}".format(sentimentdir))
		print (e)
		#sys.exit(1)

	with open(arg, 'r') as fulljson, open(fname1, 'w') as ss, open(face_rating_file, 'r') as face_file:
		dir_graph = nx.DiGraph()
		sentiment_count = Counter()
		face_dict = {}
		try:
			for single_line in fulljson:
				tweet = json.loads(single_line)
				temp_user_id = str(tweet['user']['id'])
				if tweet['user']['id'] not in tweet:
					continue
				'''
				Strip each line of the \n and/or \r characters
				'''
				#face_file_list = [line.rstrip('\n\r') for line in face_file]
				#face_file_list = face_file.read().split('\n')

				'''
				Read each line of the file and convert it into a dictionary.
				Then get the user_id string to be compared 
				with the "user_id" value from the JSON file containing the tweets.
				Only the tweets that belong to the user_id's in the face_file are stored.
				'''
				for split_file in face_file:
					#face_details = json.loads(face_single_line.replace('\r\n', ''))
					#face_details = face_single_line.readline()
					split_line = split_file.split()
					face_dict[split_line[0]] = {split_line[1:]:split_line[2:]}
					print (face_dict)
					if temp_user_id == face_rating:
						sentiment_score = calculate_sentiment(tweet['text'])
						attention_score = float(calculate_attention(tweet))
						#print (sentiment_score)
						#print ("Attention score:" + str(attention_score))
						print (temp_user_id + " has a sentiment score " + sentiment_score)
						if 'id' in tweet:
							try:
								ss.write(json.dumps(tweet) + "\n")
								#dir_graph.add_node(tweet['id'], tweet_text=tweet['text'], user_id=tweet['user']['id'], sentiment=sentiment_score)
								dir_graph.add_node(tweet['id'], tweet_text=tweet['text'], user_id=tweet['user']['id'], sentiment=sentiment_score, attention = attention_score)
								if tweet['in_reply_to_status_id']:
									reply_to_original = tweet['in_reply_to_status_id']
									#if reply_to_original in dir_graph and tweet['user']['id'] != dir_graph.node[reply_to_original][user_id]:
									if reply_to_original in dir_graph:
										dir_graph.add_edge(tweet['in_reply_to_status_id'], tweet['id'])
								
							except Exception as e:
								print(e)
						
				'''
				The average sentiment score for each user should be calculated thus:
				Take the sentiment score for the tweet and assign a counter to count the number
				of positive, negative and neutral tweets... The average can then be found.
				'''
			ss.write(json.dumps(nx.info(dir_graph) + "\n"))
			print (nx.info(dir_graph))
			nx.draw(dir_graph)

			#avg_sentiment= []
				#for (p,d) in nx.nodes(data=True):
					#if dir_graph[user_id] == 
				#else
					#print(user_id NOT found:337456932)
		except Exception as e:
			print(e)
	ss.close()
	fulljson.close()

