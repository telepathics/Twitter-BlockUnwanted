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

followers = list(twitterAPI.get_followers_ids()['ids'])

def mute(user):
	try:
		twitterAPI.create_mute(user_id=user["id"])
		print(RED + "muted" + ENDC + " {} (@{}).".format(user["name"], user["screen_name"]))
	except TwythonRateLimitError:
		print("uh oh")
		sys.exit()

	time.sleep(1)


# for notFollowingID in (followers - following):
# 	user = twitterAPI.show_user(user_id=notFollowingID)

# 	sys.stdout.write("{} ({})".format(user['screen_name'], user['name']))
# 	if input().lower() == "n":
# 		continue

# 	mute(user)
# 	print()

unwanted = {}
for ID in followers[:70]:
	user = twitterAPI.show_user(user_id=ID)
	unwanted[("{} (@{})".format(user['name'], user['screen_name']))] = user

if len(unwanted) > 0:
	chosen = Picker(
		title = 'Select accounts to mute',
		options = list(unwanted.keys())
	).getSelected()

	if chosen:
		for key in chosen:
			user = unwanted[key]
			mute(user)