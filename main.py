import os, sys
import time
from twython import Twython, TwythonError, TwythonRateLimitError, TwythonAuthError
from picker import *

twitterAPI = Twython(os.environ["TWITTER_API_KEY"], os.environ["TWITTER_API_SECRET"], os.environ["TWITTER_TOKEN"], os.environ["TWITTER_TOKEN_SECRET"])


YELLOW = '\033[93m'
GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'

# ======================
#   -=- CODE TIME -=-
# ======================

followers = set(twitterAPI.get_followers_ids()['ids'])
following = set(twitterAPI.get_friends_ids()['ids'])

def block(user):
	try:
		twitterAPI.create_block(user_id=user["id"])
		print(RED + "Blocked" + ENDC + " {} (@{}).".format(user["name"], user["screen_name"]))
	except TwythonRateLimitError:
		print("uh oh")
		sys.exit()

	time.sleep(1)


# for notFollowingID in (followers - following):
# 	user = twitterAPI.show_user(user_id=notFollowingID)

# 	sys.stdout.write("{} ({})".format(user['screen_name'], user['name']))
# 	if input().lower() == "n":
# 		continue

# 	block(user)
# 	print()

unwanted = {}
for ID in followers-following:
	user = twitterAPI.show_user(user_id=ID)
	unwanted[("{} (@{})".format(user['name'], user['screen_name']))] = user

if len(unwanted) > 0:
	chosen = Picker(
		title = 'Select accounts to block',
		options = list(unwanted.keys())
	).getSelected()

	if chosen:
		for key in chosen:
			user = unwanted[key]
			block(user)
