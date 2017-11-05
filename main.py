import os, sys
import time
from twython import Twython, TwythonError, TwythonRateLimitError, TwythonAuthError
from picker import *
from keys import *

twitterAPI = Twython(twitter_api_key, twitter_api_secret, twitter_access_token, twitter_access_secret)


YELLOW = '\033[93m'
GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'

# ======================
#   -=- CODE TIME -=-
# ======================

# following = get_friends_ids
# followers = get_followers_ids
# unfriend = destroy_friendship
# block = create_block
# mute = create_mute

following = list(twitterAPI.get_friends_ids()['ids'])

def unfriend(user):
	try:
		twitterAPI.destroy_friendship(user_id=user["id"])
		print(RED + "unfriendd" + ENDC + " {} (@{}).".format(user["name"], user["screen_name"]))
	except TwythonRateLimitError:
		print("uh oh")
		sys.exit()

	time.sleep(1)


# for notFollowingID in (following - following):
# 	user = twitterAPI.show_user(user_id=notFollowingID)

# 	sys.stdout.write("{} ({})".format(user['screen_name'], user['name']))
# 	if input().lower() == "n":
# 		continue

# 	unfriend(user)
# 	print()

unwanted = {}
for ID in following[6:76]:
	user = twitterAPI.show_user(user_id=ID)
	unwanted[("{} (@{})".format(user['name'], user['screen_name']))] = user

if len(unwanted) > 0:
	chosen = Picker(
		title = 'Select accounts to unfriend',
		options = list(unwanted.keys())
	).getSelected()

	if chosen:
		for key in chosen:
			user = unwanted[key]
			unfriend(user)