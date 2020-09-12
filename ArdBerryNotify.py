from __future__ import print_function
import requests
import json
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
# If modifying these scopes, delete the file token.pickle.


def GoogleAuth(type,version,SCOPES):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(type+'.token.pickle'):
        with open(type+'.token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        input("Press any key to continue logging in to the Gmail/Google Calender")
        # Write to serial output that an error has occured
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'GoogleAuth.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(type+'.token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build(type, version, credentials=creds)

def Gmail():
    """
    Credits: Brandon Jacobson(https://www.youtube.com/watch?v=JLXfwNdJ3Es&ab_channel=BrandonJacobson) for video guide & Google for auth
    0 -> No emails
    1 -> Emails but only peak important keywords and senders list
    2 -> Emails only peak NLP extremes
    3 -> Emails that peak list and NLP extremes
    """
    # Authenticate
    service = GoogleAuth("gmail","v1","https://www.googleapis.com/auth/gmail.readonly")


    Results = service.users().messages().list(userId='me',labelIds=["INBOX"],q="is:unread").execute()
    MessageResult  = Results.get('messages',[])

    if len(MessageResult) == 0:
        return 0
    for Email in MessageResult:
        EmailData = service.users().messages().get(userId='me', id=Email['id']).execute()
        EmailSnippet = EmailData['snippet']
        Sender = ""
        Subject = ""
        for i in EmailData["payload"]["headers"]:
            if i['name'] == "From":
                Sender = i["value"][i["value"].index("<")+1:-1]
            if i["name"] == "Subject":
                Subject = i["value"]
        print(Subject+"|"+EmailSnippet+"|"+Sender)





def ClassTimes():
    # Authenticate
    service = GoogleAuth('calendar',"v3","https://www.googleapis.com/auth/calendar.readonly")
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def WeatherData():
    with open('AQI.json', 'r') as RawJson:
        KeyData = json.load(RawJson)["key"]
    req = requests.get('http://api.airvisual.com/v2/city?city=???&state=???&country=???&key='+KeyData)
    ResponseData  = json.loads(req.text)
    AQIData = ResponseData["data"]["current"]["pollution"]["aqius"]
    TempData = (ResponseData["data"]["current"]["weather"]["tp"] * (9/5)) + 32
    HumdData = ResponseData["data"]["current"]["weather"]["hu"]

    # Process UV data {'ORDER': 20, 'ZIP': 95776, 'DATE_TIME': 'SEP/11/2020 11 PM', 'UV_VALUE': 0}, {'ORDER': 21, 'ZIP': 95776, 'DATE_TIME': 'SEP/12/2020 12 AM', 'UV_VALUE': 0}
    req = requests.get("https://enviro.epa.gov/enviro/efservice/getEnvirofactsUVHOURLY/ZIP/95776/json")
    ResponseData = json.loads(req.text)


    print(str(AQIData)+" | "+ str(TempData)+" | "+str(HumdData) )

    # Convert into ints
    return []

def Forcast():
    # https://www.weather.gov/documentation/services-web-api
    header = {"User-Agent": "(???, ???)"}
    req = requests.get('https://api.weather.gov/gridpoints/STO/31,73/forecast',headers=header)
    print(req.text)
if __name__ == "__main__":
    # ClassTimes()
    # Make sure serial output for error function is working
    # Run Api calls every 5 minutes
    # Gmail()
    #Forcast()
    #use formula for color calc for weather data
