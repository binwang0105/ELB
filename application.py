# introduce Flask
from flask import Flask, render_template
from flask import request
from pyes import *
import json


# create application object
application = Flask(__name__)

# create URL
@application.route('/', methods=['GET'])
@application.route('/hello', methods=['GET', 'POST'])
@application.route('/hello/<name>', methods=['GET', 'POST'])
def hello(name=None):
    return 'hello world!'


@application.route('/map', methods=['GET', 'POST'])
def map(name=None):
    if request.method == 'POST':
        conn = ES('127.0.0.1:9200')
        q = TermQuery("content", request.form['form'])
        results = conn.search(query = q)
        #res = format_js(res)
        #print len(results)
        tweets = []
        for r in results:
            if(not str(r['coords']) == "None"):
                #print "This is time: " + str(r['time'])
                #print "This is content: " + str(r['content'])
                #print "This is coords: " + str(r['coords'])
            	st = ""
            	st = "['" + str(r['time']) + "','" + str(r['content']) + "'," + str(r['coords']) + "]"
                tweets.append(st) 
                #print tweets
                #tweets.append(format_js(r))



        #send = "[" + "], [".join(str(", ".join(str(y) for y in x)) for x in tweets) + "]"
        send = ", ".join(str(x) for x in tweets)
        send = "[" + send + "]"
        print send
        #js array [a,b,c]
        #populate google map
        return render_template('map.html', tweets=send)
    else:
        return render_template('map.html', tweets=[])

def format_js(result):
    ret = [str(result[0].encode('ascii','ignore')),str(result[1].encode('ascii','ignore')),str(result[2].encode('ascii','ignore'))]
    return ret

# start web service
if __name__ == '__main__':
    application.debug = False 
    application.run(host='0.0.0.0')
