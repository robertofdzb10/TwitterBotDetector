import tweepy

def is_bot(user):
    # Add your Twitter API credentials here
    consumer_key = "YOUR_CONSUMER_KEY"
    consumer_secret = "YOUR_CONSUMER_SECRET"
    access_token = "YOUR_ACCESS_TOKEN"
    access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

    # Authenticate with Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Get user information
    user_info = api.get_user(user)

    # Check if the user has a default profile image and a high number of followers
    if user_info.default_profile_image and user_info.followers_count > 1000:
        return True
    else:
        return False
