from tkinter import *
from datetime import datetime
from datetime import timedelta
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from os import path
from time import sleep
from PIL import ImageTk, Image
from newsapi import NewsApiClient
import pickle
import textwrap
import requests
import pycountry

if path.exists("token.pkl") == True:
    credentials = pickle.load(open("token.pkl", "rb"))
else:
    scopes = ["https://www.googleapis.com/auth/calendar"]
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
    credentials = flow.run_console()
    pickle.dump(credentials, open("token.pkl", "wb"))

service = build("calendar", "v3", credentials=credentials)

root = Tk()
root.title("S.A.M.B.H.A")
root.configure(background="#000000")
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

def getDate() :
    date = datetime.now().date()
    day = date.weekday()
    date = str(date)
    date = date.split("-")
    days = ["Monday, ", "Tuesday, ", "Wednesday, ", "Thursday, ", "Friday, ", "Saturday, ", "Sunday, "]
    months = ["", "January ", "February ", "March ", "April ", "May ", "June ", "July ", "August ", "September ", "October ", "November ", "December "]
    day = days[day]
    month = months[int(date[1])]
    output = day + month + date[2] + ", " + date[0]
    return(output)

def getTime() :
    time = datetime.now().time()
    time = str(time).split(":")
    hour = time[0]
    if(int(hour) < 12) :
        ampm = " am"
    else :
        if(int(hour)!= 12) :
            hour = str(int(hour) - 12)
        ampm = " pm"
    output = hour + ":" + time[1] + ampm
    return(output)

def getEvents() :
    result = service.calendarList().list().execute()
    now = datetime.utcnow()
    nnow = str(now).replace(" ", "T") + "Z"
    check = []
    events = []
    for i in range(0, 63, 1) :
        then = now + timedelta(days=i)
        then = str(then).replace(" ", "T") + "Z"
        events_result = service.events().list(calendarId='en.indian#holiday@group.v.calendar.google.com', timeMin=nnow,maxResults=4, timeMax=then, singleEvents=True,orderBy='startTime').execute()
        events = events_result.get('items', [])
        if(len(events)==4) :
            break
    event1 = events[(len(events)-4)]
    event2 = events[(len(events)-3)]
    event3 = events[(len(events)-2)]
    event4 = events[(len(events)-1)]
    start1 = event1['start'].get('dateTime', event1['start'].get('date'))
    start2 = event2['start'].get('dateTime', event2['start'].get('date'))
    start3 = event3['start'].get('dateTime', event3['start'].get('date'))
    start4 = event4['start'].get('dateTime', event4['start'].get('date'))
    outputEvent1 = start1 + " " + event1['summary']
    outputEvent2 = start2 + " " + event2['summary']
    outputEvent3 = start3 + " " + event3['summary']
    outputEvent4 = start4 + " " + event4['summary']
    output = [outputEvent1, outputEvent2, outputEvent3, outputEvent4]
    return(output)

def getNews() :
    newsapi = NewsApiClient(api_key='774792c0b3eb4fcaaf94cd53aeaf6cee')
    top_headlines = newsapi.get_top_headlines(country="in",language='en')
    article1 = top_headlines['articles'][0]
    article1_title = article1['title']
    output = article1_title
    return(output)

def newsWrap(headline) :
    wrapper = textwrap.TextWrapper(width=55)
    output = wrapper.wrap(text=headline)
    return(output)

def impFunction() :
    hour = int((str(datetime.now().time()).split(":"))[0])
    if((hour < 19)and(hour > 6)) :
        time = "day"
    else :
        time = "night"
    return(time)

def getWeather() :
    dayPeriod = impFunction()
    res = requests.get('https://ipinfo.io/')
    data = res.json()
    city = data['city']
    location = data['loc'].split(',')
    latitude = location[0]
    longitude = location[1]
    wres = requests.get('http://api.openweathermap.org/data/2.5/weather?lat=' + latitude + '&lon=' + longitude + '&units=metric&appid=3b42e5c6414b24b5419538e1c25cfcf3')
    wdata = wres.json()
    country = (pycountry.countries.get(alpha_2=((wdata["sys"])["country"]))).name
    place = city + ", " + country
    weatherData = wdata['weather']
    weatherData = weatherData[0]
    wmain = weatherData['main']
    wdesc = weatherData['description']
    tempdata = wdata['main']
    temp = str(tempdata['temp']) + "°C"
    icoChooser1 = ["Mist", "Smoke", "Haze", "Dust", "Fog", "Sand", "Ash"]
    icoChooser2 = ["few clouds", "scattered clouds"]
    if(wmain == "Thunderstorm") :
        icon = "Thunderstorm.png"
    elif(wmain == "Drizzle") :
        icon = "Rain.png"
    elif(wmain == "Rain") :
        icon = "Rain.png"
    elif((wmain == "Rain")and(wdesc == "freezing rain")) :
        icon = "Snow.png"
    elif("sleet" in wdesc) :
        icon = "Sleet.png"
    elif(wmain == "Snow") :
        icon = "Snow.png"
    elif(wmain in icoChooser1) :
        icon = "Mist.png"
    elif(wmain == "Tornado") :
        icon = "Tornado.png"
    elif(wmain == "Squall") :
        icon = "Squall.png"
    elif((wmain == "Clear")and(dayPeriod == "day")) :
        icon = "Clear.png"
    elif((wmain == "Clear")and(dayPeriod == "night")) :
        icon = "ClearN.png"
    elif((wdesc in icoChooser2)and(dayPeriod == "day")) :
        icon = "FewClouds.png"
    elif((wdesc in icoChooser2)and(dayPeriod == "night")) :
        icon = "FewCloudsN.png"
    else :
        icon = "Cloud.png"
    return(icon, temp, place)

def getCOVID19Info() :
    response_raw = requests.get('https://coronavirus-tracker-api.herokuapp.com/all')
    data = response_raw.json()
    confirmed = data['confirmed']
    confirmed = confirmed['locations']
    for i in range(0, 267, 1) :
        x = confirmed[i]
        y = x['country']
        if (y == 'India') :
            confirmed = x
            break
        else :
            continue
    recovered = data['recovered']
    recovered = recovered['locations']
    for i in range(0, 267, 1) :
        x = recovered[i]
        y = x['country']
        if (y == 'India') :
            recovered = x
            break
        else :
            continue
    dead = data['deaths']
    dead = dead['locations']
    for i in range(0, 267, 1) :
        x = dead[i]
        y = x['country']
        if (y == 'India') :
            dead = x
            break
        else :
            continue
    confirmed = str(confirmed['latest'])
    recovered = str(recovered['latest'])
    dead = str(dead['latest'])
    return(confirmed, dead, recovered)

def Draw() :
    covid19Info = getCOVID19Info()
    weatherInfo = getWeather()
    time = getTime()
    headline = getNews()
    headline = newsWrap(headline)
    weatherIcon = ImageTk.PhotoImage(Image.open(weatherInfo[0]))
    weatherIconPanel = Label(root, image = weatherIcon, bg="#000000")
    weatherIconPanel.photo = weatherIcon
    dateLabel = Label(root, text=getDate(), fg="#FFFFFF", bg="#000000", font="helvetica 24", anchor=W, justify=LEFT)
    timeLabel = Label(root, text=time, fg="#FFFFFF", bg="#000000", font="helvetica 54", anchor=W, justify=LEFT)
    temperatureLabel = Label(root, text=weatherInfo[1], fg="#FFFFFF", bg="#000000", font="helvetica 54", anchor=E, justify=RIGHT)
    placeLabel = Label(root, text=weatherInfo[2], fg="#FFFFFF", bg="#000000", font="helvetica 36", anchor=E, justify=RIGHT)
    covid19InfectedLabel = Label(root, text="Infected : ", fg="#FFFFFF", bg="#000000", font="helvetica 20", anchor=W, justify=LEFT)
    covid19DeadLabel = Label(root, text="Dead : ", fg="#FFFFFF", bg="#000000", font="helvetica 20", anchor=W, justify=LEFT)
    covid19RecoveredLabel = Label(root, text="Recovered : ", fg="#FFFFFF", bg="#000000", font="helvetica 20", anchor=W, justify=LEFT)
    Infected = Label(root, text=covid19Info[0], fg="#FFFFFF", bg="#000000", font="helvetica 20", anchor=W, justify=LEFT)
    Dead = Label(root, text=covid19Info[1], fg="#FFFFFF", bg="#000000", font="helvetica 20", anchor=W, justify=LEFT)
    Recovered = Label(root, text=covid19Info[2], fg="#FFFFFF", bg="#000000", font="helvetica 20", anchor=W, justify=LEFT)

    if(len(headline) == 1) :
        newsLabel1 = Label(root, text=headline[0], fg="#FFFFFF", bg="#000000", font="helvetica 20", anchor=W, justify=CENTER)
        newsLabel1.place(x=220, y=1260)
    elif(len(headline) == 2) :
        newsLabel1 = Label(root, text=headline[0], fg="#FFFFFF", bg="#000000", font="helvetica 20", anchor=W, justify=CENTER)
        newsLabel2 = Label(root, text=headline[1], fg="#FFFFFF", bg="#000000", font="helvetica 20", anchor=W, justify=CENTER)
        newsLabel1.place(x=220, y=1260)
        newsLabel2.place(x=(220 + (495 - (len(headline[1])*9))/2), y=1310)
    else :
        newsLabel1 = Label(root, text=headline[0], fg="#FFFFFF", bg="#000000", font="helvetica 20", anchor=W, justify=CENTER)
        newsLabel2 = Label(root, text=(headline[1] + "..."), fg="#FFFFFF", bg="#000000", font="helvetica 20", anchor=W, justify=CENTER)
        newsLabel1.place(x=220, y=1260)
        newsLabel2.place(x=153, y=1310)

    dateLabel.place(x=60, y=30)
    timeLabel.place(x=60, y=80)
    temperatureLabel.place(x=860, y=45)
    weatherIconPanel.place(x=710, y=40)
    placeLabel.place(x=770, y=200)
    covid19InfectedLabel.place(x=660, y=1610)
    covid19DeadLabel.place(x=660, y=1660)
    covid19RecoveredLabel.place(x=660, y=1710)
    Infected.place(x=780, y=1610)
    Dead.place(x=750, y=1660)
    Recovered.place(x=817, y=1710)
    root.after(20000, Draw)

eve = getEvents()
event1 = eve[0]
event2 = eve[1]
event3 = eve[2]
event4 = eve[3]

eventHeadingLabel = Label(root, text="EVENTS", fg="#FFFFFF", bg="#000000", font="helvetica 36", anchor=W, justify=LEFT)
newsHeadingLabel = Label(root, text="NEWS", fg="#FFFFFF", bg="#000000", font="helvetica 36", anchor=W, justify=LEFT)
eventLabel1 = Label(root, text=event1, fg="#FFFFFF", bg="#000000", font="helvetica 20", anchor=W, justify=LEFT)
eventLabel2 = Label(root, text=event2, fg="#FFFFFF", bg="#000000", font="helvetica 20", anchor=W, justify=LEFT)
eventLabel3 = Label(root, text=event3, fg="#FFFFFF", bg="#000000", font="helvetica 20", anchor=W, justify=LEFT)
eventLabel4 = Label(root, text=event4, fg="#FFFFFF", bg="#000000", font="helvetica 20", anchor=W, justify=LEFT)
coronavirusHeadingLabel1 = Label(root, text="CORONAVIRUS", fg="#FFFFFF", bg="#000000", font="helvetica 36", anchor=W, justify=LEFT)

eventHeadingLabel.place(x=60, y=1510)
eventLabel1.place(x=60, y=1610)
eventLabel2.place(x=60, y=1660)
eventLabel3.place(x=60, y=1710)
eventLabel4.place(x=60, y=1760)
coronavirusHeadingLabel1.place(x=660, y=1510)
newsHeadingLabel.place(x=480, y=1160)





Draw()
root.mainloop()
