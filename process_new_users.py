import requests
from private import typeform_variables, slack_variables

def get_processed_email_addresses():
    try:
        f = open('private/processed_email_addresses.txt','r')
        return f.read().splitlines()
    except:
        return []

response = requests.get(typeform_variables.full_url)
data = response.json()
processed_email_addresses = get_processed_email_addresses()


new_email_addresses = []
for x in range(0, len(data['responses'])):
    email_address = data['responses'][x]['answers']['email_8634884']
    if email_address != '' and email_address not in processed_email_addresses:
        first_name = data['responses'][x]['answers']['textfield_8634882']
        payload = {'email': email_address, 'first_name': first_name, 'token': slack_variables.api_key, 'set_active': 'true', '_attempts': 1}
        r = requests.post(slack_variables.full_url, data=payload )
        if r.text == '{"ok":true}' or r.text == '{"ok":false,"error":"already_in_team"}' or r.text == '{"ok":false,"error":"already_invited"}':
            new_email_addresses.append(email_address)
        print email_address + ' - ' + r.text

f = open('private/processed_email_addresses.txt', 'a')
for email_address in new_email_addresses:
    f.write(email_address + '\n')
