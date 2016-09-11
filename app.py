import lxml.etree as etree
from slackclient import SlackClient

SLACK_TOKEN = 'INSERT SLACK TOKEN HERE'

slack_client = SlackClient(SLACK_TOKEN)

# Change the channel's name here
channelName = 'INSERT CHANNEL NAME HERE'

# The user dictionary. If new user added, comment out the first if statement starting on line 88
# and uncomment the other if statement starting on line 104. Then execute the program, find the new user
# and his/her id, and then put the id and the username as a key/value pair in the users dictionary.
users = {'U00000000': 'bogeunchoi'}

# Used for getting public channel messages
def list_channels():
    channels_call = slack_client.api_call("channels.list")
    if channels_call.get('ok'):
        return channels_call['channels']
    return None

# Used for getting public channel messages
def get_messages():
    channels = list_channels()
    # Number corresponds to channel: test to see which channel corresponds with each number
    # Change the number in the [] according to which channel you would like info from
    c = channels[0]

    # Change the number of messages in the 'count' var where 100 currently is. 1000 is the max
    messages = slack_client.api_call("channels.history", channel=c.get('id'), count=100)
    if messages.get('ok'):
        return messages['messages']
    return None

# Used for getting direct messsages
def list_direct_messages():
    direct_messages = slack_client.api_call("im.list")
    if direct_messages.get('ok'):
        return direct_messages['ims']
    return None

# Used for getting direct messsages
def get_direct_messages():
    direct_messages = list_direct_messages()
    # Number corresponds to direct channel (depends on the user):
    # To find out which number corresponds to which channel, comment out the main method in line 88
    # and uncomment the last main method in line 111. Run the program to get the index/direct message pairings.
    d = direct_messages[4]

    # Change the number of messages in the 'count' var where 100 currently is. 1000 is the max
    messages = slack_client.api_call("im.history", channel=d.get('id'), count=100)
    if messages.get('ok'):
        return messages['messages']
    return None

# Method to make the XML file
def make_xml_file():
    messages = get_messages()
    direct_messages = get_direct_messages()

    # If you want direct messages, change every instance of messages to direct_messages (lines 66 and 70)
    # and vice versa
    if messages:
        root = etree.Element('root')
        data = etree.SubElement(root, 'data')

        for m in messages:
            user = users.get(m['user'])
            item = etree.SubElement(data, 'item')
            etree.SubElement(item, 'name').text = user
            etree.SubElement(item, 'time').text = m['ts']
            etree.SubElement(item, 'message').text = m['text']

        # Change the name of the file you want to export data to here
        path = '/Users/bchoi/Desktop/projects/slack-data-project/' + channelName + 'Data.xml'
        tree = etree.ElementTree(root)
        tree.write(path, pretty_print=True)
    else:
        print("Unable to authenticate")

if __name__ == '__main__':
    make_xml_file()
    print('XML file created')

# Helper method for main in line 101
def list_users():
    users_call = slack_client.api_call("channels.list")
    if users_call.get('ok'):
        return users_call['channels']
    return None

# Helper method for main in line 101
def get_users():
    users = list_users()
    return users

# Method to find the id corresponding to the username.
#if __name__ == '__main__':
#    users = get_users()
#    if users:
#        for u in users:
#            print(u['id'] + ": " + u['name'])

# Method to find the corresponding index for the direct messages.
#if __name__ == '__main__':
#    counter = 0
#    messages = list_direct_messages()
#    if messages:
#        for m in messages:
#            print(str(counter) + ': ' + users.get(m['user']))
#            counter = counter + 1
