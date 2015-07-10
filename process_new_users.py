import requests
from private import typeform_variables, slack_variables

def get_processed_email_addresses():
    try:
        f = open('private/processed_email_addresses.txt','r')
        return f.read().splitlines()
    except:
        return

response = requests.get(typeform_variables.full_url)
processed_email_addresses = get_processed_email_addresses()

print response.text
data = response.json()
print data
print data['stats']
print data['questions']

new_email_addresses = []
for x in range(0, len(data['responses'])):
    email_address = data['responses'][x]['answers']['email_8634884']
    if email_address != '' and email_address not in processed_email_addresses:
        new_email_addresses.append(email_address)
        first_name = data['responses'][x]['answers']['textfield_8634882']
        #last_name = data['responses'][x]['answers']['textfield_8634883']
        #print first_name + ' ' + last_name + ' - ' + email_address
        #payload = {'email': email_address, 'first_name': first_name, 'token': slack_variables.api_key, 'set_active': true, '_attempts': 1}
print "new email addresses above"

payload = {'email': 'gt50@hotmail.com', 'first_name': 'Shawn', 'token': slack_variables.api_key, 'set_active': 'true', '_attempts': 1}
r = requests.post(slack_variables.full_url, data=payload )
print r.status_code
print r.reason
print r.text
# remove duplicate email addresses
new_email_addresses = list(set(new_email_addresses))

f = open('private/processed_email_addresses.txt', 'a')
for email_address in new_email_addresses:
    f.write(email_address + '\n')
print "File contents"
print

print slack_variables.full_url