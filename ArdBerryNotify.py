from __future__ import print_function
import requests
import json
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import serial
import re
import time
from textblob import TextBlob



def GoogleAuth(type,version,SCOPES):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    SCOPES = [SCOPES]
    if os.path.exists(type+'.token.pickle'):
        with open(type+'.token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        # Write to serial output that an error has occured
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except:
                UnexpectedFailure("Error in GoogleAuth")
                exit(1)
        else:
            PleaseLogIn()
            input("Press any key to continue logging in to the Gmail/Google Calender!")
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
    with open("ImportantSender.json", 'r') as VIPList:
        VIPS = json.load(VIPList)["VIPS"]
    with open("ImportantKeywords.json", 'r') as WordList:
        KeyWords = json.load(WordList)["KeyWords"]
    NLPHit = False
    ImportantKeywordOrSender = False
    if len(MessageResult) == 0:
        return 0
    for Email in MessageResult:
        EmailData = service.users().messages().get(userId='me', id=Email['id']).execute()
        EmailSnippet = EmailData['snippet']
        Sender = ""
        Subject = ""
        for i in EmailData["payload"]["headers"]:
            if i['name'] == "From":
                Sender = i["value"][i["value"].index("<")+1:-1].lower()
            if i["name"] == "Subject":
                Subject = i["value"]
        # Analysis portion, only try if a hit hasn't been found
        if not NLPHit:
            EmailTextAnalysis = TextBlob((Subject + EmailSnippet).lower())
            EmailTextPol = EmailTextAnalysis.sentiment.polarity
            EmailTextOpi = EmailTextAnalysis.sentiment.subjectivity
            print(EmailTextOpi)
            print(EmailTextPol)
            if (EmailTextOpi < 0.25 or EmailTextOpi == 1) and (
                    EmailTextPol > 0.8 or EmailTextPol < -0.5 or EmailTextPol == 0):
                NLPHit = True

        # Sender and Keyword  check, only try if a hit hasn't been found
        if not ImportantKeywordOrSender:
            EmailTextAnalysis = (Subject + EmailSnippet).lower()
            for Word in KeyWords:
                if Word in EmailTextAnalysis:
                    ImportantKeywordOrSender = True
            for Person in VIPS:
                if re.search(Person, Sender):
                    ImportantKeywordOrSender = True


    if ImportantKeywordOrSender and NLPHit:
        return 3
    elif ImportantKeywordOrSender:
        return 1
    else:
        return 2




def DoIHaveClass():
    # Authenticate
    service = GoogleAuth('calendar',"v3","https://www.googleapis.com/auth/calendar.readonly")
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    time.sleep(1)
    window = datetime.datetime.utcnow().isoformat()  + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,timeMax=window,
                                          maxResults=1, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        return 0
    else:
        return 1

def IsTheWeatherBad():
    # +33 for single char conversion
    with open('AQI.json', 'r') as RawJson:
        KeyData = json.load(RawJson)["key"]
    try:
        req = requests.get('http://api.airvisual.com/v2/city?city=Woodland&state=California&country=USA&key='+KeyData)
    except:
        UnexpectedFailure("Error in Swiss AQI API")
        exit(1)
    ResponseData  = json.loads(req.text)
    AQIData = int(ResponseData["data"]["current"]["pollution"]["aqius"] > 100)
    TempData = int(((ResponseData["data"]["current"]["weather"]["tp"] * (9/5)) + 32) > 90)
    HumdData = int(ResponseData["data"]["current"]["weather"]["hu"] > 60)
    WindData = int(round(ResponseData["data"]["current"]["weather"]["ws"]) > 17)
    try:
        req = requests.get("https://enviro.epa.gov/enviro/efservice/getEnvirofactsUVHOURLY/ZIP/95776/json")
    except:
        UnexpectedFailure("Error in UV API")
        exit(1)
    ResponseData = json.loads(req.text)

    Hour24 = re.search("[0-9]{2}:",str(datetime.datetime.now())).group()[:-1]
    Hour24 = datetime.datetime.strptime(Hour24, "%H")
    Hour12= Hour24.strftime("%I %p")
    UVData = -1
    for SingleUVForecast in ResponseData:
        if re.search("[0-9][0-9] [AP]M",SingleUVForecast["DATE_TIME"]).group() == Hour12:
            UVData = int(SingleUVForecast["UV_VALUE"] >= 6)
            break

    # Debug lines:
    # print(str(AQIData)+" | "+ str(TempData)+" | "+str(HumdData) +" | "+str(UVData))
    # print(str(ord(AQIData)-33) + " | " + str(ord(TempData)-33) + " | " + str(ord(HumdData)-33) + " | " + str(ord(UVData)-33))

    # Convert into weighted int
    return int(((AQIData*50) + (TempData*30) + (HumdData*5) + (UVData*30) + (WindData*20)) > 50)

def Forcast():
    # https://www.weather.gov/documentation/services-web-api
    header = {"User-Agent": "(ArdBerryNotify, ismaildee@gmail.com)"}
    try:
        req = requests.get('https://api.weather.gov/gridpoints/STO/31,73/forecast',headers=header)
    except:
        UnexpectedFailure("Error in Forecast API")
        exit(1)
    Result = json.loads(req.text)
    Forecast = Result["properties"]["periods"][0]["detailedForecast"][0:93]
    return [chr(len(Forecast) + 33), Forecast]

def LCDUpdate():
    pass
    # Fix when on Raspberry PI 4
    # LCDUpdate waits for 5 minutes afterwards tell people an update  is happening(set some counter) -> while doing
    # that scroll output text at a good enough pace that it repeats a couple of times

def UnexpectedFailure(ErrorDescription):
    pass
    # Pass serial output to arduino also pass in Error description in place of forcast data
    # Will force arduino to shutdown all current processes(turn all lights red) -> follow same format as data format

    # Will turn Raspberry PI's LCD to error state prompt
    exit(1)

def PleaseLogIn():
    pass
    # Pass serial output to arduino
    # Will force arduino to shutdown all current processes(turn all lights red) -> follow same format as data format
    # Will turn Raspberry PI's LCD to error state prompt


if __name__ == "__main__":
    pass

    # Run Api calls every 5 minutes
    # Data will be sent to the arduino and LCD in a standardized format -> for error and data purposes
    # Error "lights" is taken care by the arduino code -> still be able to accept data in case of gmail/calendar auth

    # Make sure all apis are working and LCDUpdate works
    # Make sure serial output for error function is working
