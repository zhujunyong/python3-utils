# -*- coding: utf-8 -*-


import datetime

def printDate():
    today = datetime.date.today()

    yesterday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)

    print(yesterday, today, tomorrow)



