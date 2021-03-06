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
r.set("aj-optionA","0")
r.set("aj-optionB","0")
countOptionA = r.get("aj-optionA")
countOptionB = r.get("aj-optionB")

@app.route('/')
def Presso():

    return """
    <html>

    <head>
    <link href="static/css/lightbox.css" rel="stylesheet">
    </head>

    <body bgcolor="LightSlateGray">

    <center><h1><font color="white">Interactive Presso<br/>
    </center>

    <center>
    <a href="/static/Slide1.JPG" data-lightbox="Presso"><img src="/static/Slide1.JPG" alt="Slide #1"></a>
    <a href="/static/Slide2.JPG" data-lightbox="Presso"></a>
    <a href="/static/Slide3.JPG" data-lightbox="Presso"></a>
    <a href="/static/Slide4.JPG" data-lightbox="Presso"></a>
    <a href="/static/Slide5.JPG" data-lightbox="Presso"></a>
    <a href="/static/Slide6.JPG" data-lightbox="Presso"></a>
    </center>

    <center><br/>
    <h1>Vote Now!</h1>
    <h2>http://interactivepresso-aj.cfapps.io/vote</h2><br/>
    <button type="button" onclick="getVotes()">Update Votes</button>
    <div id="votesFor"><h2>Votes for A<br/>
    Votes for B</h2></div>
    </center>

    <center>
    <table>
    <tr>
    <td><center>
    <h1><font color="white">Option A<br/>
    <a href="/static/Slide8.JPG" data-lightbox="OptionA"><img src="/static/Slide8.JPG" alt="Slide #8" height="270" width="450"></a>
    <a href="/static/Slide9.JPG" data-lightbox="OptionA"></a>
    <a href="/static/Slide10.JPG" data-lightbox="OptionA"></a>
    </center></td>

    <td><center>
    <h1><font color="white">Option B<br/>
    <a href="/static/Slide11.JPG" data-lightbox="OptionB"><img src="/static/Slide11.JPG" alt="Slide #11" height="270" width="450"></a>
    <a href="/static/Slide12.JPG" data-lightbox="OptionB"></a>
    <a href="/static/Slide13.JPG" data-lightbox="OptionB"></a>
    </center></td>
    </tr>
    </table>
    </center>

    <script src="/static/js/lightbox-plus-jquery.js"></script>

    <script>
    function getVotes() {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
            document.getElementById("votesFor").innerHTML = xhttp.responseText;
            }
        };
    xhttp.open("GET", "/getVotes", true);
    xhttp.send();
    }

    </script>
    </body>
    </html>
    """

@app.route('/vote')
def UserInteraction():

    return """
    <html>
    <body bgcolor="LightSlateGray">

    <center><h1><font color="white">Voting Page</h1><br/>

    <button type="button" onclick="voteA()">Vote for Track A</button>
    <button type="button" onclick="voteB()">Vote for Track B</button>

    <div id="votesForA"><h2>Votes for A</h2></div>
    <div id="votesForB"><h2>Votes for B</h2></div>
    </center>

    <script>
    function voteA() {
        var xhttpA = new XMLHttpRequest();
        xhttpA.onreadystatechange = function() {
            if (xhttpA.readyState == 4 && xhttpA.status == 200) {
            document.getElementById("votesForA").innerHTML = xhttpA.responseText;
            }
        };
    xhttpA.open("GET", "/voteA", true);
    xhttpA.send();
    }

    function voteB() {
        var xhttpB = new XMLHttpRequest();
        xhttpB.onreadystatechange = function() {
            if (xhttpB.readyState == 4 && xhttpB.status == 200) {
            document.getElementById("votesForB").innerHTML = xhttpB.responseText;
            }
        };
    xhttpB.open("GET", "/voteB", true);
    xhttpB.send();
    }
    </script>

    </body>
    </html>
    """

@app.route('/voteA')
def votedForA():

    global countOptionA
    countOptionA = r.incr("aj-optionA")

    return """
    <h2>Votes for A {}</h2>
    """.format(countOptionA)

@app.route('/voteB')
def votedForB():

    global countOptionB
    countOptionB = r.incr("aj-optionB")

    return """
    <h2>Votes for B {}</h2>
    """.format(countOptionB)

@app.route('/getVotes')
def votesFor():

    getOptionA = r.get("aj-optionA")
    getOptionB = r.get("aj-optionB")

    return """
    <h2>Votes for A {}<br/>
    Votes for B {}</h2>
    """.format(getOptionA,getOptionB)

if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
