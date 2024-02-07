import tweepy

consumer_key = 'xaAGJ3rdMvAm3BoVCHerP0URN'
consumer_secret = 'zs1aeYCh6jqLKxWDRpTYKGluSEx1uQcOAlW5SZNurgimWA3g3T'
access_token = '1620805543588659202-OslPg3bRdGo5LarmovdOb6cRT1IiHM'
access_token_secret = '850499qFFWCUgcamX56OW8A4Nkx1FELBRyoB2wEmEs2ar'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


trending_hashtags = api.get_place_trends(id=23424922, count=10)[0]['trends']

# Display the trending hashtags on the console
for i, hashtag in enumerate(trending_hashtags, start=1):
    print(f"{i}. {hashtag['name']}")
