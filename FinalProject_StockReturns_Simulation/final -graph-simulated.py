'''
import csv
from nlib import *
filename = 'aapl.csv'

with open(filename) as myfile:
    reader = csv.reader(myfile)
    header = reader.next()
    rows = [dict(zip(header,row)) for row in reader]
    for row in rows:
        print row['Date'], float(row['Adj Close'])

'''

import csv
import datetime
import math
#from nlib import *

filename = 'fb.csv'
start_date = datetime.datetime(2013,5,28) 
end_date = datetime.datetime(2018,5,25)
now = datetime.datetime.now()
history = []#store days, close price
log_returns = []
with open(filename) as myfile:
    reader = csv.reader(myfile)
    header = reader.next()
    rows = [dict(zip(header,row)) for row in reader]
    rows.reverse()
    for k,row in enumerate(rows):        
        date = datetime.datetime.strptime(row['Date'], '%m/%d/%Y')        
        close = float(row['Adj Close'])
        if k>1:
            log_return = math.log(close/previous_close)
        else:
            log_return = 0.0
        if start_date < date < end_date: 
            history.append([(date-start_date).days, close])#---> x=num of days, y
            log_returns.append(log_return)
            print date, close, log_return
        previous_close = close

mu = mean(log_returns)
sigma = sd(log_returns)
        
print mu, sigma#-4.46, 0.016--->sigma is daily volatility-->fluctuation

canvas = Canvas()
canvas.plot(history)
for scenario in range(1):
    future = []
    last_day, P = history[-1]#last price
    for k in range(1,252):#next100 days
        Rt =  random.gauss(mu, sigma)
        P = P*exp(Rt) 
        future.append([last_day+k, P])
        canvas.plot(future, color='red')
canvas.save('fb1.png')
Canvas().hist(log_returns).save('fb.log.hist.png')