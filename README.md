A program to get the messages from channels in the SSEC MetObs Slack group.

To use, you must get a virtual environment. To do so, go to the directory
with all of the slack-data-project files and put in 'virtualenv venv' in the
terminal, which will create a folder with all of the files necessary to create
a virtual environment.

Once that is done, activate the virtualenv by putting in 'source venv/bin/activate'
in the terminal, which should make the prompt look something like this: (venv)$

Install slackclient by calling 'pip install slackclient==1.0.0'. Now, you must
get your test token by going to this site: (https://api.slack.com/docs/oauth-test-tokens)
and generating your test token. Once you have generated the token, copy it and then
in your terminal, type 'python' to activate python. Then, type the following 
into the terminal, copying your test token into where 'your test token here' is:

from slackclient import SlackClient

slack_client = SlackClient('your test token here')

slack_client.api_call("api.test")

The terminal should return something in the format of this: {u'args': {u'token': u'xoxp-361113305843-7621238052-8691112296227-d0d4824abe'}, u'ok': True}

Enter one more test to authenticate: 'slack_client.api_call("auth.test")'
It should return something in the format of this: {u'user_id': u'U0S77S29J', u'url': u'https://fullstackguides.slack.com/', u'team_id': u'T0S8V1ZQA', u'user': u'matt', u'team': u'Full Stack Guides, u'ok': True}

Finally, install a final program by typing 'pip install lxml' into the terminal. 

The program should now work. To select the channel you want to get messages 
from, on the app.py file, change the channelName variable on line 9 in app.py. 
Then on line 34 or 55 (depending on whether you're getting data from the 
channels or direct messages), change the index of the channels list, where each 
number corresponds to a different channel (for more info, see file comments). 
Then execute app.py using 'python app.py'. That xml file should be located in the 
SSEC MetObs directory. Copy the XML file into the slack-data-project directory.

In the xml_to_pdf.py file, on line 12, edit the channelName variable to be the 
name of the channel you are getting the XML data from. Then execute the 
xml_to_pdf.py program using 'python xml_to_pdf.py'. A pdf of the data from the 
XML file should be created.

Note: if new users are added on Slack, please refer to app.py on adding a new 
user. Also refer to app.py when changing the file you want to put data into and 
refer to xml_to_pdf.py when changing the xml file to extract from/changing
the name of the pdf you want to create.

Thanks to Matt Makai for his tutorial on using Python and Flask for the Slack
API, which was a great help for this program: https://realpython.com/blog/python/getting-started-with-the-slack-api-using-python-and-flask/