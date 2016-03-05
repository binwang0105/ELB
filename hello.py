from pyes import *

import tweepy

consumer_key        = "Jj01lVEbPn8fupbiXphhmOxON"
consumer_secret     = "iVYTRTZ4hbgh0zIvdxzzMMLFZbha5MPnD61qfgZm0koOvanbYL"
access_token        = "704740943539339264-P6c1QHN7L5F5pku9cwUvmtIisuza7HO"
access_token_secret = "dX327UZ65ofhGB3UIhQGJMJPGw7UQ2233q9hnGkuYVirL"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

mapping = {
        'time': {
            'boost': 1.0,
            'index': 'analyzed',
            'store': 'yes',
            'type': 'string',
            "term_vector": "with_positions_offsets"
        },
        'content': {
            'boost': 1.0,
            'index': 'analyzed',
            'store': 'yes',
            'type': 'string',
            "term_vector": "with_positions_offsets"
        },
        'coords': {
            'boost': 1.0,
            'index': 'analyzed',
            'store': 'yes',
            'type': 'string',
            "term_vector": "with_positions_offsets"
        }
    }

def main():

    conn = ES('127.0.0.1:9200')
    try:
        conn.indices.delete_index("test-index")
    except:
        pass
    conn.indices.create_index("test-index")
    conn.indices.put_mapping("test-type", {'properties':mapping}, ["test-index"])

    i = 1

    for tweet in tweepy.Cursor(api.search,
                           q="Curry OR Trump OR Car",
                           count=100,
                           result_type="recent",
                           include_entities=True,
                           lang="en").items():

        if(tweet.geo):
            coords = tweet.geo['coordinates']
            conn.index({"time":tweet.created_at, "content":tweet.text.strip().encode('ascii','ignore'), "coords":str(coords)}, "test-index", "test-type", i)
        else:
            conn.index({"time":tweet.created_at, "content":tweet.text.strip().encode('ascii','ignore'), "coords":"None"}, "test-index", "test-type", i)
        i=i+1
        if(i>10000):
            break;
            


    ''' Attributes of tweet:
    ['__class__', '__delattr__', '__dict__', '__doc__', '__format__', 
    '__getattribute__', '__getstate__', '__hash__', '__init__', '__module__', 
    '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', 
    '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_api', 
    '_json', 'author', 'contributors', 'coordinates', 'created_at', 'destroy',
     'entities', 'favorite', 'favorite_count', 'favorited', 'geo', 'id', 
     'id_str', 'in_reply_to_screen_name', 'in_reply_to_status_id', 
     'in_reply_to_status_id_str', 'in_reply_to_user_id', 
     'in_reply_to_user_id_str', 'lang', 'metadata', 'parse', 'parse_list', 
     'place', 'possibly_sensitive', 'retweet', 'retweet_count', 'retweeted',
      'retweets', 'source', 'source_url', 'text', 'truncated', 'user']
    '''

    
    conn.indices.refresh("test-index")

        
    q = TermQuery("content", "good")
    results = conn.search(query = q)
    print len(results)
    for r in results:
        print r

if __name__ == '__main__':
    main()