import time
#replace the following two lines with your apikey from slack and your team name
api_key = 'xoxp-slack-api-key'
host_name = 'team-name'


full_url = 'https://' + host_name + '.slack.com/api/users.admin.invite?t=' + str(int(time.time()))