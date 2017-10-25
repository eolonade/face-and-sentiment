import os
import tweepy
import sys
from twitter_client import get_twitter_auth
from collections import Counter
import json
import wget
from twitter_client import get_twitter_client
from tweepy import Cursor
import time
import urllib3
import urllib
import requests
from PIL import Image #Done by installing the pillow package
# from StringIO import StringIO
from io import StringIO # BytesIO can also be used
import shutil

api = get_twitter_client()

def paginate(items, n):
	"""Generate n-sized chunks from items"""
	for i in range(0, len(items), n):
		yield items[i:i+n]

def get_user_mentions(tweet_details):
	try:
		entities = tweet_details.get('entities', {})
		mentions = entities.get('user_mentions', [])
		return [tag['id_str'] for tag in mentions]
	except Exception as e:
		print(e)

# Since there is a limit of 100 IDs, the user ids should be given
# in steps of 100
##def get_user_images(id_list):
	##try:
		##for ids in range(0, len(id_list), int(len(id_list)/100)):
			##user_objects = api.lookup_users(id_list)
			##for user in user_objects:
				##return (user.id, user.profile_image_url)
			##if len(ids) == 3000:
				##print("More results available... Sleeping to avoid hitting the rate limit")
				##time.sleep(60)
	##except Exception as e:
		##print(e)

if __name__ == '__main__':
	arg = sys.argv[1]
	auth = get_twitter_client()


	dirname = "users/{}".format(arg)
	imgdir = "users/{}/user_images/".format(arg)
	id_files = 'users/{}/id.jsonl'.format(arg)
	image_url_files = 'users/{}/image_url.jsonl'.format(arg)
	fname1 = "users/{}/id_and_url_list.jsonl".format(arg)
	fname2 = "users/{}/top_500_url_and_id.jsonl".format(arg)
	fname3 = "users/{}/top_500_users_id.jsonl".format(arg)
	try:
		os.makedirs(dirname, mode=0o755, exist_ok=True)
		os.makedirs(imgdir, mode=0o755, exist_ok=True)
	except OSError:
		print("Directory {} already exists". format(dirname))	
	except Exception as e:
		print("Error while creating directory {}".format(dirname))
		print("Error while creating directory {}".format(imgdir))
		print(e)
		sys.exit(1)


	# Get each line of the jsonl file as a json file
	
	top_user_list = []
	all_user_url_list = []
	top_user_url_list = []
	user_list = []
	with open(arg, 'r') as o:
		with open(fname1, 'w') as f:
			users = []
			for line in o:
				try:
					tweet = json.loads(line)
					#for line in f:
					#If the line below doesn't work when importing to MongoDB, 
					#I think I'll have to remove the 'str' casting function
					#It might have conveted the file to an unsuitable format
					temp_user_id = str(tweet['user']['id'])
					temp_url = str(tweet['user']['profile_image_url']).replace('normal','400x400')
					users = {"user_id" : temp_user_id, "url": temp_url}
					#user = '{"id": "tweet['user']['id_str']", "image_url": "tweet['user']['profile_image_url']"}'				
					##user = str(("id: "+ tweet['user']['id_str'], "image_url: "+ tweet['user']['profile_image_url']))
					#user = auth.get_user('user_id')
					#user = auth.lookup_users('user_id')
					#user_list =	','.join(user)
					#user= user.replace('normal','400x400')
					#user_list = json.loads(user)
					##user_list =	''.join(user)
					#user_list.append(user)
					user_json = ""
					#user_image_url.append(user)
					#user_json.append([[str(user_list) for users in tweet] for line in o])
					user_json = json.dumps(users)				
					#user_json = json.dumps([ for user_list in users] for line in o)
					f.write(user_json + "\n")
					print(user_json) #, user_image_url)
						#time.sleep(5)
					#f.write(user_list)
				except Exception as e:
					print(e)
			o.close()
		f.close()

	
	# Get each line of the jsonl file as a json file
	##with open(arg, 'r') as o:
			##with open(fname2, 'w') as f:
				##for line in o:
					##try:
						##tweet = json.loads(line)
						##user_image_url_list = object()
						#for line in f:
						#If the line below doesn't work when importing to MongoDB, 
						#I think I'll have to remove the 'str' casting function
						#It might have conveted the file to an unsuitable format
						##user = str(tweet['user']['profile_image_url'])
						##user= user.replace('normal','400x400')
						##user_image_url_list = ''.join(user)
							#user_list.append(user)
							#user_image_url.append(user)
						##print(user_image_url_list) #, user_image_url)
							#time.sleep(5)
						##f.write((user_image_url_list) + "\n")
					##except Exception as e:
						##print(e)
			##f.close()
	##o.close()
	
		##for user, count in top_user_count.most_common(10):
			##top_user_list.append(user)
			#print("{}: {}".format(user, count))
		##print(all_user_url_list['user_id'])


	# Get all tweets as from the JSONL file (the one with all tweets)
	# For each tweet, check for user mentions
	# Store the IDs of the top 500 users with the highest mentions
	# For each ID, get the corresponding url from the 'id_and_url_file'
	# Download the images of these 500 users

 	# For every line in the original file, get the id and url and update the counter
	# Store these values as a JSON object (has been done earlier in the code - fname1)
	# For every line in the id_and_url_file variable, check if the 'user_id' == mentions_list['id']

	with open(arg, 'r') as original_file, open(fname1, 'r') as id_and_url_file, open(fname2, 'w') as top_500_id_and_count_file, open(fname3, 'w') as id_and_count_500_file:

		try:
			top_user_count = Counter()
			top_500 = []
			number_of_mentions = []
			#mentions_list = []
			for line in original_file:
				tweet = json.loads(line)
				number_of_mentions = get_user_mentions(tweet)
				top_user_count.update(number_of_mentions)
			for id_str, count,  in top_user_count.most_common(500):
				print ("{},{}". format(id_str, count))
				#mentions_list.append(id_str, count)				
				#mentions_list = {"id": id_str, "count": count}
				top_500.append(id_str)
			print (top_500)
			top_500_id_and_count_file.write(json.dumps(top_user_count) + "\n")
			id_and_count_500_file.write(json.dumps(top_500) + "\n")
		except Exception as e:
			print(e)
	original_file.close()
	id_and_url_file.close()
	id_and_count_500_file.close()

	# Another approach
	# ----------------
	# Save the urls as a file or as a list and get users by ID
	# The whole user data doesn't have to be extracted, just the URL
	# The image can then be downloaded.

	#with open(fname1, 'r') as id_and_url_file, open(fname3, 'r') as id_and_count_500_file:
		#for ids in id_and_count_500_file:
			#print (ids)
			#print(ids["id"])
			#ids_json = json.loads(ids)
			#for urls in id_and_url_file:
				#urls_json = json.loads(urls)
				#if ids_json["id"] == urls_json["user_id"]:
					#print(urls_json["url"])
					#print()

	##http = urllib3.PoolManager()
	#urls = http.request('GET', fname2, preload_content = False)
	##with open(arg, 'r') as u:
		##for line in u:
			##tweet = json.loads(line)
			#mentions_in_tweet = get_user_mentions(tweet)
	img_id = []
	http = urllib3.PoolManager()				
	with open(fname3, 'r') as id_and_count_500_file:
		try:
			print(top_500)
			print("Top 500 images printed")
			#img_id = get_user_images(top_500)
			#for ids in range(0, len(top_500), len((top_500)/100)):
			for pages in id_and_count_500_file:
				for chunk in paginate(top_500, 100):
						user_objects = api.lookup_users(user_ids=chunk)
						for user in user_objects:
							#return (user.id, user.profile_image_url)
							number = user.id
							img_url = str(user.profile_image_url).replace('normal', '400x400')
							with open(imgdir + str(number) + ".jpg", 'wb')  as i:
								url = requests.get(img_url, stream=True)
								shutil.copyfileobj(url.raw, i)
							i.close()
						if len(top_500) == 3000:
							print("More results available... Sleeping to avoid hitting the rate limit")
							time.sleep(60)
		except Exception as e:
			print(e)
	id_and_count_500_file.close()
			





