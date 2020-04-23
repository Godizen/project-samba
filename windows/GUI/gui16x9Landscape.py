'''

THIS SCRIPT IS FOR A
16:9 ASPECT RATIO MONITOR
IN LANDSCAPE

'''

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
import requests
from bs4 import BeautifulSoup

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
xCoordsMultiplier = (root.winfo_screenwidth() / 1920)
yCoordsMultiplier = (root.winfo_screenheight() / 1080)
fontSizeMultiplier = xCoordsMultiplier
imgSizeMultiplier = xCoordsMultiplier * yCoordsMultiplier

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
    for i in range(0, 32, 1) :
        then = now + timedelta(days=i)
        then = str(then).replace(" ", "T") + "Z"
        events_result = service.events().list(calendarId='en.indian#holiday@group.v.calendar.google.com', timeMin=nnow,maxResults=2, timeMax=then, singleEvents=True,orderBy='startTime').execute()
        events = events_result.get('items', [])
        if(len(events)==2) :
            break
    event1 = events[(len(events)-1)]
    event2 = events[(len(events)-2)]
    start1 = event1['start'].get('dateTime', event1['start'].get('date'))
    start2 = event2['start'].get('dateTime', event2['start'].get('date'))
    outputEvent1 = start1 + " " + event1['summary']
    outputEvent2 = start2 + " " + event2['summary']
    output = [outputEvent1, outputEvent2]
    return(output)

def getNews() :
    newsapi = NewsApiClient(api_key='774792c0b3eb4fcaaf94cd53aeaf6cee')
    top_headlines = newsapi.get_top_headlines(country="in",language='en')
    article1 = top_headlines['articles'][0]
    article1_title = article1['title']
    article2 = top_headlines['articles'][1]
    article2_title = article2['title']
    output = [article1_title, article2_title]
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

def getTimeofDay() :
    hour = int((str(datetime.now().time()).split(":"))[0])
    minute = int((str(datetime.now().time()).split(":"))[1])
    if((hour == 6)and(minute == 0)) :
        output = 'Morning'
    elif((hour == 12)and(minute == 0)) :
        output = 'Noon'
    elif((hour == 18)and(minute == 0)) :
        output = 'Evening'
    elif((hour == 0)and(minute == 0)) :
        output = 'Midnight'
    else :
        output = 'None'
    return(output)

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
    temp = str(int(tempdata['temp'])) + "°C"
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

    infected=0
    dead=0
    recovered=0

    for i in range(0, len(stats)) :
        infected = infected + int(stats[i][3])
        dead = dead + int(stats[i][5])
        recovered = recovered + int(stats[i][4])

    infected = 'Infected : ' + str(infected)
    dead = 'Dead : ' + str(dead)
    recovered = 'Recovered : ' + str(recovered)
    return(infected, dead, recovered)

eventHeadingLabel = Label(root, text="EVENTS", fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 38))), anchor=W, justify=LEFT)
newsHeadingLabel = Label(root, text="NEWS", fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 38))), anchor=W, justify=LEFT)
coronavirusHeadingLabel = Label(root, text="CORONAVIRUS LIVE", fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 38))), anchor=W, justify=LEFT)

eventHeadingLabel.place(x=(60 * xCoordsMultiplier), y=(300 * yCoordsMultiplier))
coronavirusHeadingLabel.place(x=(1360 * xCoordsMultiplier), y=(450 * yCoordsMultiplier))
newsHeadingLabel.place(x=(60 * xCoordsMultiplier), y=(600 * yCoordsMultiplier))

def Draw(e1=None, e2=None, eventLabels=True) :
    try :
        if(eventLabels is True) :
            eve = getEvents()
            event1 = eve[0]
            event2 = eve[1]
            covid19Info = getCOVID19Info()
            weatherInfo = getWeather()
            time = getTime()
            headlines = getNews()
            headline1 = newsWrap(headlines[0])
            headline2 = newsWrap(headlines[1])
            wIcon = Image.open(weatherInfo[0])
            wIcon = wIcon.resize(((int(100 * imgSizeMultiplier)), (int(100 * imgSizeMultiplier))), Image.ANTIALIAS)
            weatherIcon = ImageTk.PhotoImage(wIcon)
            weatherIconPanel = Label(root, image = weatherIcon, bg="#000000")
            weatherIconPanel.photo = weatherIcon
            dateLabel = Label(root, text=getDate(), fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 24))), anchor=W, justify=LEFT)
            timeLabel = Label(root, text=time, fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 54))), anchor=W, justify=LEFT)
            eventLabel1 = Label(root, text=event1, fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
            eventLabel2 = Label(root, text=event2, fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
            temperatureLabel = Label(root, text=weatherInfo[1], fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 54))), anchor=E, justify=RIGHT)
            placeLabel = Label(root, text=weatherInfo[2], fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 36))), anchor=E, justify=RIGHT)
            Infected = Label(root, text=covid19Info[0], fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
            Dead = Label(root, text=covid19Info[1], fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
            Recovered = Label(root, text=covid19Info[2], fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)

            if(len(headline1)==1) :
                newsLabel1 = Label(root, text=("1. " + headline1[0]), fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
                newsLabel1.place(x=(60 * xCoordsMultiplier), y=(700 * yCoordsMultiplier))
            elif(len(headline1)==2) :
                newsLabel1 = Label(root, text=("1. " + headline1[0]), fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
                newsLabel2 = Label(root, text=headline1[1], fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
                newsLabel1.place(x=(60 * xCoordsMultiplier), y=(700 * yCoordsMultiplier))
                newsLabel2.place(x=(60 * xCoordsMultiplier), y=(750 * yCoordsMultiplier))
            else :
                newsLabel1 = Label(root, text=("1. " + headline1[0]), fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
                newsLabel2 = Label(root, text=(headline1[1] + "..."), fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
                newsLabel1.place(x=(60 * xCoordsMultiplier), y=(700 * yCoordsMultiplier))
                newsLabel2.place(x=(60 * xCoordsMultiplier), y=(750 * yCoordsMultiplier))

            if(len(headline2)==1) :
                newsLabel3 = Label(root, text=("2. " + headline2[0]), fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
                newsLabel3.place(x=(60 * xCoordsMultiplier), y=(850 * yCoordsMultiplier))
            elif(len(headline2)==2) :
                newsLabel3 = Label(root, text=("2. " + headline2[0]), fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
                newsLabel4 = Label(root, text=headline2[1], fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
                newsLabel3.place(x=(60 * xCoordsMultiplier), y=(850 * yCoordsMultiplier))
                newsLabel4.place(x=(60 * xCoordsMultiplier), y=(900 * yCoordsMultiplier))
            else :
                newsLabel3 = Label(root, text=("2. " + headline2[0]), fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
                newsLabel4 = Label(root, text=(headline2[1] + "..."), fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
                newsLabel3.place(x=(60 * xCoordsMultiplier), y=(850 * yCoordsMultiplier))
                newsLabel4.place(x=(60 * xCoordsMultiplier), y=(900 * yCoordsMultiplier))

            dateLabel.place(x=(60 * xCoordsMultiplier), y=(30 * yCoordsMultiplier))
            timeLabel.place(x=(60 * xCoordsMultiplier), y=(80 * yCoordsMultiplier))
            eventLabel1.place(x=(60 * xCoordsMultiplier), y=(400 * yCoordsMultiplier))
            eventLabel2.place(x=(60 * xCoordsMultiplier), y=(450 * yCoordsMultiplier))
            temperatureLabel.place(x=(1714 * xCoordsMultiplier), y=(45 * yCoordsMultiplier))
            weatherIconPanel.place(x=(1564 * xCoordsMultiplier), y=(40 * yCoordsMultiplier))
            placeLabel.place(x=int((((1920 - ((len(weatherInfo[2]) * (17 * fontSizeMultiplier) + 106))) * xCoordsMultiplier))), y=(200 * yCoordsMultiplier))
            Infected.place(x=int((((1920 - ((len(covid19Info[0]) * (9 * fontSizeMultiplier) + 106))) * xCoordsMultiplier))), y=(550 * yCoordsMultiplier))
            Dead.place(x=int((((1920 - ((len(covid19Info[1]) * (9 * fontSizeMultiplier) + 106))) * xCoordsMultiplier))), y=(600 * yCoordsMultiplier))
            Recovered.place(x=int(((((1920 - ((len(covid19Info[2]) * (9 * fontSizeMultiplier) + 106))) - 20 ) * xCoordsMultiplier))), y=(650 * yCoordsMultiplier))
            if((len(headline1)==2)and(len(headline2)==2)) :
                root.after(20000, lambda : Delete(dateLabel, timeLabel, w3=temperatureLabel, w4=weatherIconPanel, w5=placeLabel, w6=Infected, w7=Dead, w8=Recovered, w9=newsLabel1, w10=newsLabel3, w11=newsLabel2, w12=newsLabel4, w13=eventLabel1, w14=eventLabel2))
            elif(len(headline1)==2) :
                root.after(20000, lambda : Delete(dateLabel, timeLabel, w3=temperatureLabel, w4=weatherIconPanel, w5=placeLabel, w6=Infected, w7=Dead, w8=Recovered, w9=newsLabel1, w10=newsLabel3, w11=newsLabel2, w13=eventLabel1, w14=eventLabel2))
            elif(len(headline2)==2) :
                root.after(20000, lambda : Delete(dateLabel, timeLabel, w3=temperatureLabel, w4=weatherIconPanel, w5=placeLabel, w6=Infected, w7=Dead, w8=Recovered, w9=newsLabel1, w10=newsLabel3, w11=newsLabel4, w13=eventLabel1, w14=eventLabel2))
            else :
                root.after(20000, lambda : Delete(dateLabel, timeLabel, w3=temperatureLabel, w4=weatherIconPanel, w5=placeLabel, w6=Infected, w7=Dead, w8=Recovered, w9=newsLabel1, w10=newsLabel3, w13=eventLabel1, w14=eventLabel2))
        else :
            covid19Info = getCOVID19Info()
            weatherInfo = getWeather()
            time = getTime()
            headlines = getNews()
            headline1 = newsWrap(headlines[0])
            headline2 = newsWrap(headlines[1])
            wIcon = Image.open(weatherInfo[0])
            wIcon = wIcon.resize(((int(100 * imgSizeMultiplier)), (int(100 * imgSizeMultiplier))), Image.ANTIALIAS)
            weatherIcon = ImageTk.PhotoImage(wIcon)
            weatherIconPanel = Label(root, image = weatherIcon, bg="#000000")
            weatherIconPanel.photo = weatherIcon
            dateLabel = Label(root, text=getDate(), fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 24))), anchor=W, justify=LEFT)
            timeLabel = Label(root, text=time, fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 54))), anchor=W, justify=LEFT)
            temperatureLabel = Label(root, text=weatherInfo[1], fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 54))), anchor=E, justify=RIGHT)
            placeLabel = Label(root, text=weatherInfo[2], fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 36))), anchor=E, justify=RIGHT)
            Infected = Label(root, text=covid19Info[0], fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
            Dead = Label(root, text=covid19Info[1], fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
            Recovered = Label(root, text=covid19Info[2], fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)

            if(len(headline1)==1) :
                newsLabel1 = Label(root, text=("1. " + headline1[0]), fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
                newsLabel1.place(x=(60 * xCoordsMultiplier), y=(700 * yCoordsMultiplier))
            elif(len(headline1)==2) :
                newsLabel1 = Label(root, text=("1. " + headline1[0]), fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
                newsLabel2 = Label(root, text=headline1[1], fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
                newsLabel1.place(x=(60 * xCoordsMultiplier), y=(700 * yCoordsMultiplier))
                newsLabel2.place(x=(60 * xCoordsMultiplier), y=(750 * yCoordsMultiplier))
            else :
                newsLabel1 = Label(root, text=("1. " + headline1[0]), fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
                newsLabel2 = Label(root, text=(headline1[1] + "..."), fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
                newsLabel1.place(x=(60 * xCoordsMultiplier), y=(700 * yCoordsMultiplier))
                newsLabel2.place(x=(60 * xCoordsMultiplier), y=(750 * yCoordsMultiplier))

            if(len(headline2)==1) :
                newsLabel3 = Label(root, text=("2. " + headline2[0]), fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
                newsLabel3.place(x=(60 * xCoordsMultiplier), y=(850 * yCoordsMultiplier))
            elif(len(headline2)==2) :
                newsLabel3 = Label(root, text=("2. " + headline2[0]), fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
                newsLabel4 = Label(root, text=headline2[1], fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
                newsLabel3.place(x=(60 * xCoordsMultiplier), y=(850 * yCoordsMultiplier))
                newsLabel4.place(x=(60 * xCoordsMultiplier), y=(900 * yCoordsMultiplier))
            else :
                newsLabel3 = Label(root, text=("2. " + headline2[0]), fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
                newsLabel4 = Label(root, text=(headline2[1] + "..."), fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 20))), anchor=W, justify=LEFT)
                newsLabel3.place(x=(60 * xCoordsMultiplier), y=(850 * yCoordsMultiplier))
                newsLabel4.place(x=(60 * xCoordsMultiplier), y=(900 * yCoordsMultiplier))

            dateLabel.place(x=(60 * xCoordsMultiplier), y=(30 * yCoordsMultiplier))
            timeLabel.place(x=(60 * xCoordsMultiplier), y=(80 * yCoordsMultiplier))
            temperatureLabel.place(x=(1714 * xCoordsMultiplier), y=(45 * yCoordsMultiplier))
            weatherIconPanel.place(x=(1564 * xCoordsMultiplier), y=(40 * yCoordsMultiplier))
            placeLabel.place(x=int((((1920 - ((len(weatherInfo[2]) * (17 * fontSizeMultiplier) + 106))) * xCoordsMultiplier))), y=(200 * yCoordsMultiplier))
            Infected.place(x=int((((1920 - ((len(covid19Info[0]) * (9 * fontSizeMultiplier) + 106))) * xCoordsMultiplier))), y=(550 * yCoordsMultiplier))
            Dead.place(x=int((((1920 - ((len(covid19Info[1]) * (9 * fontSizeMultiplier) + 106))) * xCoordsMultiplier))), y=(600 * yCoordsMultiplier))
            Recovered.place(x=int(((((1920 - ((len(covid19Info[2]) * (9 * fontSizeMultiplier) + 106))) - 20 ) * xCoordsMultiplier))), y=(650 * yCoordsMultiplier))
            if((len(headline1)==2)and(len(headline2)==2)) :
                root.after(20000, lambda : Delete(dateLabel, timeLabel, w3=temperatureLabel, w4=weatherIconPanel, w5=placeLabel, w6=Infected, w7=Dead, w8=Recovered, w9=newsLabel1, w10=newsLabel3, w11=newsLabel2, w12=newsLabel4, w13=e1, w14=e2))
            elif(len(headline1)==2) :
                root.after(20000, lambda : Delete(dateLabel, timeLabel, w3=temperatureLabel, w4=weatherIconPanel, w5=placeLabel, w6=Infected, w7=Dead, w8=Recovered, w9=newsLabel1, w10=newsLabel3, w11=newsLabel2, w13=e1, w14=e2))
            elif(len(headline2)==2) :
                root.after(20000, lambda : Delete(dateLabel, timeLabel, w3=temperatureLabel, w4=weatherIconPanel, w5=placeLabel, w6=Infected, w7=Dead, w8=Recovered, w9=newsLabel1, w10=newsLabel3, w11=newsLabel4, w13=e1, w14=e2))
            else :
                root.after(20000, lambda : Delete(dateLabel, timeLabel, w3=temperatureLabel, w4=weatherIconPanel, w5=placeLabel, w6=Infected, w7=Dead, w8=Recovered, w9=newsLabel1, w10=newsLabel3, w13=e2, w14=e2))
    except Exception as drawError:
        print('drawError : ' + str(drawError))
        root.after(20000, Draw(eventLabels))

def Delete(w1, w2, w3=None, w4=None, w5=None, w6=None, w7=None, w8=None, w9=None, w10=None, w11=None, w12=None, w13=None, w14=None) :
    try :
        w1.destroy()
        w2.destroy()
        Draw2(w3=w3, w4=w4, w5=w5, w6=w6, w7=w7, w8=w8, w9=w9, w10=w10, w11=w11, w12=w12, w13=w13, w14=w14)
    except Exception as deleteError:
        print('deleteError : ' + str(deleteError))
        root.after(20000, lambda : Delete(w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11=w11, w12=w12, w13=w13, w14=w14))

def Draw2(w3=None, w4=None, w5=None, w6=None, w7=None, w8=None, w9=None, w10=None, w11=None, w12=None, w13=None, w14=None) :
    try :
        timePeriod = getTimeofDay()

        if(timePeriod=='Midnight') :
            Delete2(w3, w4, w5, w6, w7, w8, w9, w10, w11=w11, w12=w12, w13=w13, w14=w14)
            Draw(eventLabels=True)
        elif(not(timePeriod=='None')) :
            Delete2(w3, w4, w5, w6, w7, w8, w9, w10, w11=w11, w12=w12, w13=None, w14=None)
            Draw(e1=w13, e2=w14, eventLabels=False)
        else :
            dateLabel = Label(root, text=getDate(), fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 24))), anchor=W, justify=LEFT)
            timeLabel = Label(root, text=getTime(), fg="#FFFFFF", bg="#000000", font=("helvetica " + str(int(fontSizeMultiplier * 54))), anchor=W, justify=LEFT)
            dateLabel.place(x=(60 * xCoordsMultiplier), y=(30 * yCoordsMultiplier))
            timeLabel.place(x=(60 * xCoordsMultiplier), y=(80 * yCoordsMultiplier))
            root.after(20000, lambda : Delete(dateLabel, timeLabel, w3=w3, w4=w4, w5=w5, w6=w6, w7=w7, w8=w8, w9=w9, w10=w10, w11=w11, w12=w12, w13=w13, w14=w14))
    except Exception as arnavMessedUp :
        print('arnavMessedUp : ' + str(arnavMessedUp))

def Delete2(w3, w4, w5, w6, w7, w8, w9, w10, w11=None, w12=None, w13=None, w14=None) :
    try :
        w3.destroy()
        w4.destroy()
        w5.destroy()
        w6.destroy()
        w7.destroy()
        w8.destroy()
        w9.destroy()
        w10.destroy()
        if(not(w11 is None)) :
            w11.destroy()
        if(not(w12 is None)) :
            w12.destroy()
        if(not(w13 is None)) :
            w13.destroy()
        if(not(w14 is None)) :
            w14.destroy()
    except Exception as deleteError2 :
        print('deleteError2 : ' + str(deleteError2))





Draw(eventLabels=True)
root.mainloop()
