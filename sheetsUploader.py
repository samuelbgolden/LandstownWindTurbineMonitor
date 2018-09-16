from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from time import sleep
import datetime

from random import randint

SPREADSHEET_ID = '1skWnHPVjPbtSoVOfgbBhB7S8VZHbb356O71nRXgXz-M'  # id of the spreadsheet to be written to, can be found in the web address: https://docs.google.com/spreadsheets/d/SPREADSHEETID/

########################################## FIRST CONNECTION (CHECKING HOW MANY LINES THERE ARE) ######################################################################
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'  # this is the permissions being granted to the action; this scope in particular allows all actions
store = file.Storage('credentials.json')  #this line and the line below do something necessary to set up a connection to the Google API Client
creds = store.get()
if not creds or creds.invalid:  # this checks if the credentials were set up correctly in the line above, and if they weren't:
	flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)  # it creates those credentials by reauthenticating (this creats a new JSON file and generally requires opening a browser
	creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))  # finally the connection is set up

########################################## SECOND CONNECTION (SUBMITTING CURRENT SENSOR DATA) ######################################################################
store2 = file.Storage('credentials2.json')                                   # all of this is the 
creds2 = store2.get()                                                        # same as above, except
if not creds2 or creds2.invalid:                                             # that it is configuring
	flow2 = client.flow_from_clientsecrets('client_secret.json', SCOPES) # a new connection, but
	creds2 = tools.run_flow(flow2, store2)                               # the process is exactly
service2 = build('sheets', 'v4', http=creds2.authorize(Http()))              # the same



while True:
    RANGE_NAME = 'Sheet1'  # because we want to see all the rows in the sheet, our range is just the sheet name                                                   
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME, majorDimension='ROWS').execute()  # this actually executes the query to the google client
    values = result.get('values', [])  # gets only the values in the spreadsheet from the list of items in the 'result' object
    #print(values)  # prints the returned spreadsheet values
    rowCurrent = len(values) + 1  # calculates the row to be written to
    
    RANGE_NAME = 'Sheet1!A{}:C{}'.format(rowCurrent, rowCurrent)  # since we are now writing to a specific place in the sheet, we now set our range to the specific space necessary for the sensor data 
    value_input_option = 'USER_ENTERED'  # this specifies that the data should be entered as it is in the string (which means our datetime string will be formatted to google sheets datetime format)
    
    # ~~~~~VALUES GO HERE~~~~~ \/
    body = { 	'values': [
                    [str(datetime.datetime.now()), randint(0,40), randint(55,95)],
                   #[CURRENT DATETIME, WIND SPEED, TEMPERATURE, ETC...],
            ],
            }
    # ~~~~~VALUES GO HERE~~~~~ /\
    
    request = service2.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME, valueInputOption=value_input_option, body=body).execute()  # the actual append request to the google client
    #print(request)  # prints the submitted request
    
    sleep(10)
