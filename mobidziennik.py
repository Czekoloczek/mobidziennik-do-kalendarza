from robobrowser import RoboBrowser
#from bs4 import BeautifulSoup
import re
import yaml
import os

#Check if the config file exists, if not, create it
configFile = 'config.yaml'
data = {}
if not os.path.isfile(configFile):
    with open(configFile, 'w') as f:
        yaml.dump({}, f)
else:
    with open(configFile, 'r') as f:
        data = yaml.safe_load(f)

while True:
    schoolSubdomain = input('Podaj subdomenę szkoły (np. jeśli URL strony twojego dziennika to \"lo1olesnica.mobidziennik.pl\", wpisz \"lo1olesnica\").\nJeśli nie podasz żadnej, program spróbuje wykorzystać zapisane dane: \n')
    if schoolSubdomain == '':
        if 'schoolSubdomain' in data:
            schoolSubdomain = data['schoolSubdomain']
        else:
            while True:
                schoolSubdomain = input('Nie znaleziono subdomeny w pliku konfiguracyjnym, wpisz ją manualnie:\n')
                if schoolSubdomain == '':
                    continue
                else:
                    break

    br = RoboBrowser(parser="html.parser")
    #Check if subdomain is correct
    try:
        br.open(f'https://{schoolSubdomain}.mobidziennik.pl/dziennik/')
        break
    except Exception as e:
        print(f"Nie udało się połączyć z serwerem. Sprawdź, czy podana subdomena jest poprawna. Błąd: {e}")

#Save the school subdomain in the config file (Note/Todo: This updates the subdomain even if it was used before, this should only happen if you manually input the subdomain)
with open(configFile, 'w') as f:
    data['schoolSubdomain'] = schoolSubdomain
    yaml.dump(data, f)
form = br.get_form()

while True:
    login = input("Podaj e-mail lub login.\nJeśli nie podasz żadnego, program spróbuje wykorzystać zapisane dane: ")
    if login == '':
        if 'login' in data:
            login = data['login']
        else:
            while True:
                login = input('Nie znaleziono loginu w pliku konfiguracyjnym, wpisz go manualnie:\n')
                if login == '':
                    continue
                else:
                    break

    form['login'] = login
    form['haslo'] = input("Podaj hasło: ")

    br.submit_form(form)
    br.open(f'https://{schoolSubdomain}.mobidziennik.pl/dziennik/planzajec/?bez-zastepstw=1')
    # Check if the user is logged in
    pageText = br.response.text

    if "Zaloguj się" in pageText:
        print("Podane dane logowania są nieprawidłowe. Spróbuj ponownie.")
    else:
        break

#Save the login in the config file
with open(configFile, 'w') as f:
    data['login'] = login
    yaml.dump(data, f)


def determineDay(percent):
    percent = str(percent)
    if percent == '0.5':
        return 0
    elif percent == '20.5':
        return 1
    elif percent == '40.5':
        return 2
    elif percent == '60.5':
        return 3
    elif percent == '80.5':
        return 4
    else:
        return 'error'


numOfLessons = i = numOfMatches = 0

calendar = {}
for bigDiv in br.find_all(class_='plansc_cnt_w'):
    numOfLessons += 1
    bigDiv = str(bigDiv)

    # RegEx the left value, ex.: style="width:19%;left:   two digits + (maybe)dot + (maybe) digit       %;"
    percent = re.search(r'style="width:\d\d%;left:(\d{1,2}.?\d?)%;', bigDiv)[1]

    title = re.search(
        r'title="(?P<startTime>\d\d:\d\d) - (?P<endTime>\d\d:\d\d)&lt;br /&gt;(?P<name>.*)&lt;br /&gt;(?P<info>.*) (?P<classroom>\(.*\))"', bigDiv)

    # get start, end, name, classroom, which day it is and additional info
    try:
        i += 1
        dayNum = determineDay(percent)
        startTime = title[1]
        endTime = title[2]
        name = title[3]
        info = title[4]
        classroom = title[5]
    except TypeError:
        pass

    # this is done for comparing number of tries against succeeded results
    try:
        title[0]
        numOfMatches += 1
    except:
        pass

    # save to dict
    calendar[numOfMatches] = {
        'name': name,
        'dayNum': dayNum,
        'startTime': startTime,
        'endTime': endTime,
        'classroom': classroom,
        'info': info,
    }

from icalendar import Calendar, Event
from datetime import datetime, date, timedelta
#import pytz
import random
import string

c = Calendar()
e = Event()

c.add('prodid', '-//JakubKoralewski//github.com//')
c.add('version', '2.0')


def randomWord(length):
    letters = string.ascii_letters
    return ''.join((random.choice(letters)) for i in range(length))


for i in calendar.keys():
    e = Event()
    name = calendar[i]['name']
    dayNum = int(calendar[i]['dayNum'])
    startTime = calendar[i]['startTime']
    endTime = calendar[i]['endTime']
    classroom = calendar[i]['classroom']
    info = calendar[i]['info']
    todaysDate = datetime.today()
    todaysDay = date.isoweekday(todaysDate)
    uid = str(todaysDate).replace(" ", "") + \
        str(randomWord(8))+'@github.com'

    # split 14:36 into 14 and 36
    startHour = int(startTime[0:2])
    startMinutes = int(startTime[3:6])
    endHour = int(endTime[0:2])
    endMinutes = int(endTime[3:6])

    # get the day from which to start adding
    mondayDelta = todaysDay - 1
    firstMonday = todaysDate - timedelta(days=mondayDelta)

    # print(firstMonday)
    summary = '{} - {}'.format(name, classroom)
    crlf = chr(13)+chr(10)
    description = '{}\r\nLekcja: {}\r\nKlasa: {}'.format(
        info, name, classroom)

    event_date = firstMonday + timedelta(days=dayNum)
    year = event_date.year
    month = event_date.month
    day = event_date.day
    #print('day: {}'.format(day))

    e.add('summary', summary)
    e.add('description', description)
    e.add('dtstart', datetime(year, month, day, startHour, startMinutes))
    e.add('dtend', datetime(year, month, day, endHour, endMinutes))
    e.add('uid', uid)
    e.add('dtstamp', todaysDate)
    if month >= 9:
        e.add('rrule', {'freq': 'weekly', 'until': datetime(year+1, 6, 30)})
    else:
        e.add('rrule', {'freq': 'weekly', 'until': datetime(year, 6, 30)})

    c.add_component(e)
    print(summary)

with open('calendar.ics', 'wb') as calendar:
    print(
        f'Twoje lekcje zostały wyeksportowane do pliku {os.getcwd() + chr(92) + "calendar.ics"}.')
    calendar.write(c.to_ical())
    input('Naciśnij cokolwiek, aby zamknąć...')
