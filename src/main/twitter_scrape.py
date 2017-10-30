import os
import io
import sys
import json
import tweepy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from collections import OrderedDict
from collections import Counter
from itertools import chain
from twitter_sentiment import calculate_sentiment


driver = webdriver.Chrome()


'''
Get the text file containing the facial attractiveness ratings
and convert it to JSONL with the keys: topic, user_id and face_score
'''
def convert_file_to_json(topic):
    topic_ratings = "topics/{}.txt".format(topic)
    topic_ratings_jsonl = "topics/{}_score.jsonl".format(topic)
    keys = ['topic', 'user_id','face_score']

    with open(topic_ratings, 'r') as a, open(topic_ratings_jsonl, 'w') as j:
        for line in a:
            entities = line.split()
            e = dict(zip(keys, entities)) #maps the keys to a corresponding value
            # Just dump it as a JSON object
            #print(e)
            j.write(json.dumps(e) + "\n")
    j.close()
    a.close()

def save_details_to_json():
    pass

# Calculte the sentiment of the tweets and replies
def calculate_sentiment(url):
    pass

# Calculate the attention based on the number of replies, retweets and "likes"
def calculate_attention(url):
    pass
'''
def get_page_elements_selenium(url):
    # Retrieve the tweet page
    driver.get(full_url)
    page_source = driver.page_source
    #get_tweet_page(ids)
    #tweets_html_page = driver.find_elements_by_class_name('js-original-tweet')
    whole_conversation = driver.find_elements_by_class_name('PermalinkOverlay-modal') #id is permalink-overlay-dialog

    
    for conversation in whole_conversation:
        original_tweet = conversation.find_element_by_class_name('TweetTextSize--jumbo')
        #original_tweet_id = conversation.find_element_by_css_selector("div.data-associated-tweet-id")
        replies_count = conversation.find_element_by_class_name('ProfileTweet-action--reply')
        retweet_count = conversation.find_element_by_class_name('ProfileTweet-action--retweet')
        like_count = conversation.find_element_by_class_name('ProfileTweet-action--favorite')
        print(original_tweet.text)
        #print(tweet_id)
        print(replies_count.text)
        print(retweet_count.text)
        print(like_count.text)
        all_replies = conversation.find_elements_by_css_selector('permalink-replies')
        #reply_replies_text = conversation.find_element_by_class_name('ThreadedConversation-tweet')
        for reply in all_replies:
            #print(reply_replies_text)
            #reply_replies_text = reply.find_element_by_class_name('js-stream-item')
            print(reply.text)
            #reply_text = reply.find_element_by_class_name('ThreadedConversation-tweet')
            #lone_tweet_reply_text = reply.find_element_by_class_name('ThreadedConversation-loneTweet')
            #print(reply_text.text)
'''
def get_page_elements(url):
    driver.get(url)
    entire_page = driver.page_source
    return entire_page
# Get the required details and store it as a JSON object
def get_tweet_details(source):
    soup =  BeautifulSoup(source, 'html.parser')
    tweet_details = {}
    for conversation in soup.select("div.PermalinkOverlay-modal"):
        # Get tweet ID, Conversation ID, User ID, Username, and the users mentioned in the tweet
        original_tweet_div = conversation.select("div.PermalinkOverlay-content > div > div > div.permalink.light-inline-actions.stream-uncapped.has-replies.original-permalink-page > div.permalink-inner.permalink-tweet-container > div")
        if original_tweet_div[0]['data-tweet-id'] is not None and len(original_tweet_div[0]['data-tweet-id']) > 0 :
            tw_tweet_id = original_tweet_div[0]['data-tweet-id']
        else:
            pass
        if original_tweet_div[0]['data-conversation-id'] is not None:
            tw_conversation_id = original_tweet_div[0]['data-conversation-id']
        if original_tweet_div[0]['data-user-id'] is not None:
            tw_user_id = original_tweet_div[0]['data-user-id']
        if original_tweet_div[0]['data-name'] is not None:
            tw_user_name = original_tweet_div[0]['data-name']
        if original_tweet_div[0]['data-reply-to-users-json'] is not None:
            tw_reply_to_users = original_tweet_div[0]['data-reply-to-users-json']

        
        if conversation is not None:
            tweet_details = {
                "conversation_id": tw_conversation_id,
                "tweet_id": tw_tweet_id,
                "user_id": tw_user_id,
                "user_name": tw_user_name,
                "tweet_text": None, 
                "reply_count": 0,
                "retweet_count": 0,
                "favorite_count": 0,
                "tweet_sentiment_score": 0.0,
                "tweet_attention_score": 0.0,
                "user_attractiveness_score": 0.0,
                "reply_to_user": tw_reply_to_users,
                "replies": {
                    "tweet_id": None,
                    "user_id": None,
                    "tweet_text": None,
                    "tweet_sentiment_score": None,
                    #"tweet_attention_score": None,
                    #"tweet_attractiveness_score": None,
                    "reply_to_user": None # JSON object expected
                }
            }
        '''
        # Get tweet text
        tweet_text_p = conversation.select("div.PermalinkOverlay-content > div > div > div.permalink.light-inline-actions.stream-uncapped.has-replies.original-permalink-page > div.permalink-inner.permalink-tweet-container > div > div.js-tweet-text-container > p")
        if tweet_text_p is not None:
            tw_tweet_text = tweet_text_p[0]['tweet-text']
        
        # Select reply count
        tw_reply = conversation.select("div.PermalinkOverlay-content > div > div > div.permalink.light-inline-actions.stream-uncapped.has-replies.original-permalink-page > div.permalink-inner.permalink-tweet-container > div > div.stream-item-footer > div.ProfileTweet-actionCountList.u-hiddenVisually > span.ProfileTweet-action--reply.u-hiddenVisually > span.ProfileTweet-actionCount")
        if tw_reply is not None and len(tw_reply) > 0:
            tw_reply_count = int(tw_reply[0]['data-tweet-stat-count'])
            print(tw_reply_count)

        # Select retweet count
        tw_retweet = conversation.select("div.PermalinkOverlay-content > div > div > div.permalink.light-inline-actions.stream-uncapped.has-replies.original-permalink-page > div.permalink-inner.permalink-tweet-container > div > div.stream-item-footer > div.ProfileTweet-actionCountList.u-hiddenVisually > span.ProfileTweet-action--retweet.u-hiddenVisually > span.ProfileTweet-actionCount")
        if tw_retweet is not None and len(tw_retweet) > 0:
            tw_retweet_count = int(tw_retweet[0]['data-tweet-stat-count'])
            print(tw_retweet_count)

        # Select favorite count
        tw_favorite = conversation.select("div.PermalinkOverlay-content > div > div > div.permalink.light-inline-actions.stream-uncapped.has-replies.original-permalink-page > div.permalink-inner.permalink-tweet-container > div > div.stream-item-footer > div.ProfileTweet-actionCountList.u-hiddenVisually > span.ProfileTweet-action--favorite.u-hiddenVisually > span.ProfileTweet-actionCount")
        if tw_favorite is not None and len(tw_favorite) > 0:
            tw_favorite_count = int(tw_favorite[0]['data-tweet-stat-count'])
            print(tw_favorite_count)

        '''
        print (tweet_details)
    print("=====================")
    

    # Add sentiment score
    # Add attention score. Attention score = (no of replies + no of retweets + no of "likes")/no of followers
    # The number of followers might have to be added in another function. It has to be gotten using the API. 
    # So it might be ignored for now.

'''
This function takes in the JSON file for a single tweet and returns 
a list containing the tweet_id, and the ID and the username of 
the author.
'''
'''
def get_ids(tweet):
    try:
        id_list = []
        tw_tweet_id = str(tweet['id'])
        tw_user_id = str(tweet['user']['id'])
        tw_username = str(tweet['user']['screen_name']) 
        # To Do: Also check for user mentions because that was the basis on which
        # users were downloaded
        #tw_mentions = str(tweet['entities']['user_mentions'])
        id_list = [tw_tweet_id, tw_user_id, tw_username]
        return (id_list)
    except KeyError:
        pass
'''
'''
def get_tweet_page(id_list):
    # If the user_id does not exist, then proceed to the next object
    if not id_list[1]:
        pass
    base_url = "https://twitter.com/{}/status/".format(id_list[2])

    status_id = id_list[0]
    full_url = base_url+status_id
    # Retrieve the tweet page
    driver.get(full_url)

    tweets = driver.find_elements_by_tag_name('tweet-text')
    for tweet in tweets:
        print(tweet)
'''


'''
# Both the topic and user ID should be used to make sure
# the same user isn't considered multiple times for every topic.
# Actually, I don't think that would happen since each topic would
# be considered in isolation and both keys would be checked.
A user that would be able to have an effect on more than a topic 
is the user that has been active about both topics.
'''


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print ("Usage: python3 {} <filename> <Topic(e.g. DemoTopic)>".format(argv[0]))
    fname = sys.argv[1]
    topic = sys.argv[2]

    # Get the attractiveness scores
    faces_json = convert_file_to_json(topic)
    topic_ratings_file = "topics/{}_score.jsonl".format(topic)
    # A file for testing some output values
    utility_file = "utility_{}.jsonl".format(topic)


    '''
    Load a JSONL file. Each line in this file would be a
    valid JSON object
    '''
    with open(fname, 'r') as all_tweets, open(utility_file, 'w') as utility:
        utility_list = []
        #no_of_appearances = Counter()
        for tw in all_tweets:
            tweet = json.loads(tw)
            # Get the tweet and user ids from which the url will be formed.
            #ids = get_ids(tweet)
            #get_tweet_page(ids)
            try:
                id_list = []
                tw_tweet_id = str(tweet['id'])
                tw_user_id = str(tweet['user']['id'])
                #tw_username = str(tweet['user']['screen_name']) 
                #tw_mentions = str(tweet['entities']['user_mentions'])
            except KeyError:
                pass
            #print (ids)
            with open(topic_ratings_file, 'r') as j: # Load the JSONL file containing the ratings
                for face_line in j:
                    each = json.loads(face_line)
                    face_user_id = each['user_id']
                    #print(face_user_id)
                    # Compare both user_id values and only get tweet elements if they do
                    if tw_user_id == str(face_user_id):
                        utility_list.append(face_user_id)
                        #no_of_appearances.update(face_user_id['user_id'])

                        '''
                        Get Tweet page
                        '''
                        if not (tw_tweet_id or tw_user_id):
                            pass
                        base_url = "https://twitter.com/{}/status/".format(tw_user_id)
                        full_url = base_url+tw_tweet_id
                        tweet_page_source = get_page_elements(full_url)
                        get_tweet_details(tweet_page_source)
                        #add_attractiveness_score(tweet_json)
                    else:
                        pass
                utility.write(json.dumps(utility_list) + "\n")

    utility.close()



def get_face_ratings(face_dict):
    pass


def search_for_string(tw_dict, topic):
    for key in tw_dict:
        if str(topic) == str(key):
            print (topic + " found")
        #for term in tw_dict[key]:
            #pass
                