import os, datetime
import pyttsx3
import speech_recognition
from tqdm import tqdm
from time import sleep
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from newsapi import NewsApiClient
import pickle
import pandas as pd
import requests
import random
from pprint import pprint
from os import path
import os.path
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import cv2
import os
import numpy as np
import time
import requests
from bs4 import BeautifulSoup



print("Initializing...")

if path.exists("token.pkl") == True:
    credentials = pickle.load(open("token.pkl", "rb"))
else:
    scopes = ["https://www.googleapis.com/auth/calendar"]
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
    credentials = flow.run_console()
    pickle.dump(credentials, open("token.pkl", "wb"))

service = build("calendar", "v3", credentials=credentials)

def showProgressBar():
    for i in tqdm(range(0, 50), desc="Loading", ascii=False, unit="Files"):
        sleep(1)

engine = pyttsx3.init('espeak')
voices = engine.getProperty('voices')
engine.setProperty('voice', 'english-us')
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

call = "hello"

def listenForCall():
    print("reached")
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("listening...")
        audio = r.listen(source)
    try:
        print("recognizing...")
        call = r.recognize_google(audio, language = 'en-in')
        call = call.lower()
        print(call)
    except Exception as err:
        print(err)
        speak("Repeat")
        waitForCall()

def tickerGetter(companyname) :
    companyname.replace(" ", "+")
    tres = requests.get('https://finance.yahoo.com/_finance_doubledown/api/resource/searchassist;searchTerm=' + companyname + '?device=console&returnMeta=true')
    tdata = tres.json()
    tdata = tdata["data"]
    tdata = tdata["items"]
    tdata = tdata[0]
    ticker = tdata["symbol"]
    return(ticker)

def stockUpdates(ticker) :
    date = datetime.date.today()
    data = yf.download(ticker, date)

    data = data[0:1]
    data1 = data[["Low"]]
    data2 = data[["High"]]
    low = int(data1.loc[:, "Low"])
    high = int(data2.loc[:, "High"])

    print(ticker)
    print("High = $", high)
    print("Low = $", low)
    speak(date)
    speak(("Highest share price today was about", high, "US Dollars"))
    speak(("Lowest share price today was about", low, "US Dollars"))

def getCompanyNameFromUsr():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone(device_index=1) as source:
        print("listening for company name...")
        audio = r.listen(source)
    try:
        print("recognizing...")
        cname = r.recognize_google(audio, language = 'en-in')
        print(cname)
    except Exception as err:
        print(err)
        speak("Repeat")
        getCompanyNameFromUsr()
    return cname

def weatherUpdates() :
    res = requests.get('https://ipinfo.io/')
    data = res.json()
    city = data['city']
    location = data['loc'].split(',')
    latitude = location[0]
    longitude = location[1]

    wres = requests.get('http://api.openweathermap.org/data/2.5/weather?lat=' + latitude + '&lon=' + longitude + '&units=metric&appid=3b42e5c6414b24b5419538e1c25cfcf3')
    wdata = wres.json()
    weatherData = wdata['weather']
    weatherData = weatherData[0]
    wmain = weatherData['main']
    wdesc = weatherData['description']
    tempdata = wdata['main']
    temp = tempdata['temp']

    print('Latitude =', latitude)
    print('Longitude =', longitude)
    print('City =', city)
    print(wmain)
    print('(' + wdesc + ')')
    print(temp, "C")
    speak('City is')
    speak(city)
    speak('The weather is')
    speak(wmain)
    speak('The temperature is')
    speak(temp)
    speak('Degrees Celsius')

def joke() :
    jcat = int(random.random() * 10)
    url = "https://jokeapi.p.rapidapi.com/category/Programming"
    querystring = {"format":"json"}
    headers = {'x-rapidapi-host': "jokeapi.p.rapidapi.com", 'x-rapidapi-key': "613908033fmsh28e06094388a0a1p1db36fjsn0866e6803798"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    joke = response.json()
    jtype = joke['type']
    if (jtype == 'single') :
        joke = joke['joke']
    elif (jtype == 'twopart') :
        joke = joke['setup'] + joke['delivery']
    print(joke)
    startPhrase = int(random.random() * 10)
    if ((startPhrase == 0) or (startPhrase == 1)) :
        speak('egg must joke mila')
    elif ((startPhrase == 2) or (startPhrase == 3)) :
        speak('dont laugh')
    elif ((startPhrase == 4) or (startPhrase == 5)) :
        speak('Ready?')
    elif ((startPhrase == 6) or (startPhrase == 7)) :
        speak('Ha ha ha, ye dekh')
    else :
        speak('Ha ha ha ha ha ha')
    speak(joke)

def COVID19UPDATE() :
    extract_contents = lambda row: [x.text.replace('\n', '') for x in row]
    URL = 'https://www.mohfw.gov.in/'

    SHORT_HEADERS = ['SNo', 'State','Indian-Confirmed',
                     'Foreign-Confirmed','Cured','Death']

    response = requests.get(URL).content
    soup = BeautifulSoup(response, 'html.parser')
    header = extract_contents(soup.tr.find_all('th'))

    stats = []
    all_rows = soup.find_all('tr')

    for row in all_rows:
        stat = extract_contents(row.find_all('td'))
        if stat:
            if len(stat) == 5:
                # last row
                stat = ['', *stat]
                stats.append(stat)
            elif len(stat) == 6:
                stats.append(stat)

    stats[-1][1] = "Total Cases"
    stats.remove(stats[-1])
    data=0
    for i in range(0, len(stats)) :
        data = str(data + int(stats[i][3]))
    data = data + ' active coronavirus cases in India'
    print(data)
    speak(data)

subjects = ["", "Arnav", "Krish", "Random"]

def detect_face(img) :
    faceCascade = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30))
    if (len(faces) == 0):
        return None, None
    (x, y, w, h) = faces[0]
    return gray[y:y+w, x:x+h], faces[0]

'''
def prepare_training_data(data_folder_path):
    dirs = os.listdir(data_folder_path)
    faces = []
    labels = []
    for dir_name in dirs:
        if not dir_name.startswith("s"):
            continue;
        label = int(dir_name.replace("s", ""))
        subject_dir_path = data_folder_path + "/" + dir_name
        subject_images_names = os.listdir(subject_dir_path)
        for image_name in subject_images_names:
            if image_name.startswith("."):
                continue;
            image_path = subject_dir_path + "/" + image_name
            image = cv2.imread(image_path)
            cv2.imshow("Training on image...", image)
            cv2.waitKey(100)
            face, rect = detect_face(image)
            if face is not None:
                faces.append(face)
                labels.append(label)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    return faces, labels
'''

def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

def predict(test_img):
    img = test_img.copy()
    face, rect = detect_face(img)
    label = face_recognizer.predict(face)
    label_text = subjects[label[0]]
    draw_rectangle(img, rect)
    draw_text(img, label_text, rect[0], rect[1]-5)
    return img, label_text

def faceAuthentication() :
    i = 7
    tryno = 0
    print("Please look at the camera")
    speak("Please look at the camera")
    while True:
        time.sleep(2)
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        k = cv2.waitKey(30) & 0xff
        try :
            if(i >= 5) :
                i = i - 1
                continue
            elif(i == -1) :
                z = 1
                break
            elif(i < 5) :
                tryno = tryno + 1
                p_img = predict(img)
                name = "Attempt " + str(tryno)
#                cv2.imshow(name, p_img[0])
                if(p_img[1] == "Arnav")or(p_img[1] == "Krish") :
                    z = 0
                    rec_usr = p_img[1]
                    break
                else :
                    i = i - 1
                    continue
        except :
            continue
    if (z == 0) :
        cap.release()
        cv2.destroyAllWindows()
        return(rec_usr)
    else :
        print("Unknown person detected, shutting down")
        speak("Unknown person detected, shutting down")
        exit()

def waitForCall():
    while listenForCall() == "hello":
        print(call)
        listenForCall()
    else:
        givenCmd = takeCmd()
        givenCmd = givenCmd.lower()
        if "exit" in givenCmd:
            print("exiting...")
            exit()
        elif "hello" in givenCmd:
            speak("hello")
            waitForCall()
        elif "news" in givenCmd:
            sayNews(0)
            waitForCall()
        elif "stock" in givenCmd:
            speak("Company ka naam bata")
            cnameRecieved = getCompanyNameFromUsr()
            stockUpdates(tickerGetter(cnameRecieved))
            waitForCall()
        elif "weather" in givenCmd:
            weatherUpdates()
            waitForCall()
        elif "joke" in givenCmd:
            joke()
            waitForCall()
        elif (("coronavirus" in givenCmd) or ("corona virus" in givenCmd)):
            COVID19UPDATE()
            waitForCall()
        elif ((("recognise" in givenCmd)and("my" in givenCmd))and("face" in givenCmd)) :
            auth_usr = faceAuthentication()
            waitForCall()
        elif ('volume' in givenCmd) :
            speak('Say the new volume from one to one hundred')
            vol = getNewVolume()
            engine.setProperty('volume', vol)
            waitForCall()
        elif (('what' in givenCmd)and('time' in givenCmd)) :
            time = datetime.datetime.now()
            time = str(time).split(' ')
            time = time[1]
            time = time.split(':')
            time = time[0] + time[1] + ' hours'
            print(time)
            speak(time)
            waitForCall()
        else :
            speak("Ke bol re la hai tu?")
            takeCmd()



def takeCmd():
    print("taking command")
    cmd = ""
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("listening for command...")
        audio = r.listen(source)
    try:
        print("recognizing command...")
        cmd = r.recognize_google(audio, language = 'en-in')
        print(cmd.lower())
    except Exception as error:
        print(error)
        speak("Repeat command")
        takeCmd()
    return cmd




def wish(usr):
    result = service.calendarList().list().execute()
    #print(result)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='en.indian#holiday@group.v.calendar.google.com', timeMin=now,
                                        maxResults=1, timeMax=now, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    dayPeriod = ""
    time = int(datetime.datetime.now().hour)
    if time>=0 and time<12:
        dayPeriod = "Good Morning"
    elif time>=12 and time<4:
        dayPeriod = "Good Afternoon"
    else:
        dayPeriod = "Good Evening"

    if not events:
        speak(dayPeriod + "sardhaar     " + usr)
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        speak(dayPeriod + "sardhaar     " + usr)
        speak("Happy " + event['summary'] + "Sardhaar     " + usr)



def sayNews(newsNum):
    # Init
    newsapi = NewsApiClient(api_key='774792c0b3eb4fcaaf94cd53aeaf6cee')

    # /v2/top-headlines
    top_headlines = newsapi.get_top_headlines(country="in", language='en')

    #print(top_headlines)
    articles = top_headlines['articles'][newsNum]
    article_title = articles['title']
    article_desc = articles['description']
    print("===========Title===========")
    print(article_title)
    speak(article_title)
    print("")
    print("=========Description=======")
    print(article_desc)
    speak(article_desc)
    print("")

showProgressBar()
#faces, labels = prepare_training_data("./training-data")
face_recognizer = cv2.face.createLBPHFaceRecognizer()
face_recognizer.load('recognizer.yml')
#face_recognizer.train(faces, np.array(labels))
cap = cv2.VideoCapture(0)
auth_usr = faceAuthentication()
wish(auth_usr)
waitForCall()
cap.release()
cv2.destroyAllWindows()
