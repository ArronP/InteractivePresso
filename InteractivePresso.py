import os
import uuid
from flask import Flask
import urlparse
import redis
import json

rediscloud_service = json.loads(os.environ['VCAP_SERVICES'])['rediscloud'][0]
credentials = rediscloud_service['credentials']
r = redis.Redis(host=credentials['hostname'], port=credentials['port'], password=credentials['password'])

app = Flask(__name__)
my_uuid = str(uuid.uuid1())
BLUE = "#3F0080"
GREEN = "#33CC33"
r.set("aj:incr","0")

COLOR = BLUE

@app.route('/')
def hello():

    counter = r.incr("aj:incr")

    return """
    <html>
    <body bgcolor="{}">

    <center><h1><font color="white">Hi, I'm GUID:<br/>
    {}</br>

    <center><h2><font color="white">INCREMENT:{}<br/>

    </center>

    </body>
    </html>
    """.format(COLOR,my_uuid,counter)

if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
