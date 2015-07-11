#Insert apikey and uid from typeform below
api_key = 'typeformapikey'
uid = 'typeformuid'
api_url = 'https://api.typeform.com/v0/form/'
#Add field names from your form below. Email and First name are necesary.
email_address_field = 'email_00000'
first_name_field = 'textfield_00001'
#last_name_field = 'textfield_00002'

#the commented line below only shows completed forms. The one below that shows all.
#full_url = api_url + uid + '?key=' + api_key + '&completed=true&order_by[]=date_land,desc'
full_url = api_url + uid + '?key=' + api_key + '&order_by[]=date_land,desc'
