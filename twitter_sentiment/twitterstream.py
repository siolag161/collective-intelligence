
from ConfigParser import RawConfigParser

import urllib2 as urllib
import oauth2 as oauth
_debug = 0

def oauth_req(url, token_key, token_secret,consumer_key, consumer_secret,
              params=[],http_method="GET"):

    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    token = oauth.Token(key=token_key, secret=token_secret)

    req = oauth.Request.from_consumer_and_token(consumer,
                                             token=token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=params)

    signature_method = oauth.SignatureMethod_HMAC_SHA1()
    req.sign_request(signature_method, consumer, token)

    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()

    
    http_handler  = urllib.HTTPHandler(debuglevel=_debug)
    https_handler = urllib.HTTPSHandler(debuglevel=_debug)
    
    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)
     
    return response 
    
def fetchSample():
    config_parser = RawConfigParser()
    config_parser.read("settings.cfg")
    consumer_key = config_parser.get("TwitterOAuth", "CONSUMER_KEY")
    consumer_secret = config_parser.get("TwitterOAuth", "CONSUMER_SECRET")
    access_token_key = config_parser.get("TwitterOAuth", "ACCESS_TOKEN_KEY")
    access_token_secret = config_parser.get("TwitterOAuth", "ACCESS_TOKEN_SECRET")
  
    params={'locations':'-180,-90,180,90'}
    res = oauth_req("https://stream.twitter.com/1/statuses/filter.json", access_token_key, 
              access_token_secret,consumer_key, consumer_secret, params,"POST")

    for line in res:
        print line.strip()
if __name__ == '__main__':
  fetchSample()
