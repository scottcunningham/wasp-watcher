#!/usr/bin/python
import sys
import random
import time
import datetime

customer_id = "123"

import sqlite3
conn = sqlite3.connect('example.db')

current_milli_time = lambda: int(round(time.time() * 1000))

def ms2str(milliseconds):
    hours, milliseconds = divmod(milliseconds, 3600000)
    minutes, milliseconds = divmod(milliseconds, 60000)
    seconds = float(milliseconds) / 1000
    time_str = "%i:%02i:%06.3f" % (hours, minutes, seconds)
    return time_str

def addtime(current, times, sql):
        now = current + random.randrange(0,100000)
        sql += ", (" + customer_id + ", " + str(now) + ")" 
        times.append(now)
        return sql

ONE_SECOND_MILLIS = 1000
ONE_MINUTE_MILLIS = ONE_SECOND_MILLIS * 60
ONE_HOUR_MILLIS = ONE_MINUTE_MILLIS * 60 
ONE_DAY_MILLIS = ONE_HOUR_MILLIS * 24
ONE_WEEK_MILLIS = ONE_DAY_MILLIS * 7

sql = "insert into customer_actions values"

# we want to get all timestamps from one week ago to now
current = current_milli_time() - ONE_WEEK_MILLIS  
sql += "(" + customer_id + ", " + str(current) + ")"

# the time limit is now
limit = current_milli_time()

current += 30*ONE_MINUTE_MILLIS

times = []

while True:
    
    if random.randrange(0, 4) == 3:
        sql = addtime(current, times, sql)

    if (current % ONE_DAY_MILLIS) > (ONE_HOUR_MILLIS * 21):
        current += ONE_HOUR_MILLIS * random.randrange(7, 10) # sleep for 7 - 10 hours
        sql = addtime(current, times, sql)
        continue

    if (current % ONE_DAY_MILLIS) > (ONE_HOUR_MILLIS * 23):
        current += ONE_HOUR_MILLIS * random.randrange(7, 10) # sleep for 7 - 10 hours
        sql = addtime(current, times, sql)
        continue

    if current > limit:
        break

    current = current + 30 * ONE_MINUTE_MILLIS

sql += ";"

sys.stderr.write("Produced actions at the following times:\n")
for timestamp in times:
    sys.stderr.write(datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S') + "\n")

print "Adding values to DB: "
print sql
print ""

print "Copy-paste into SQLite shell."
