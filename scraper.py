#import beautifulsoup if imported
try:
    import bs4
    from bs4 import BeautifulSoup
except ImportError as e:
    print("you do not have the beautifulsoup package")

#import marplotlib if imported
try:
    import matplotlib.pyplot as plt
except ImportError as e:
    print("you do not have the matplotlib package")

#import requests if found
try:
    import requests
except ImportError as e:
    print("you do not have the requests package")

#import lxml if found
try:
    import lxml
except ImportError as e:
    print("you do not have the lxml package")

import numpy as np

'''
#read the users input to know type of request
reply = ''
while(reply != "company" and reply != "fx"):
    print("would you like to search to search for company or fx:")
    reply = input("")
    reply.lower()

print("which asset would you like to search (use correct format)")
asset = str(input(""))
asset.upper()

if(reply == 'company'):
    path = 'https://uk.finance.yahoo.com/quote/' + asset + '/history?P=' + asset

if (reply == 'fx'):
    path = 'https://uk.finance.yahoo.com/quote/'+asset+'=X/history?p='+asset
'''
path = 'https://uk.finance.yahoo.com/quote/WORK/history?p=WORK&.tsrc=fin-srch'
asset = "work"

#Method to retrieve the page 
response = requests.get(path)
soup = bs4.BeautifulSoup(response.text, "lxml")

#extract the days and prices data from the website
daysRaw = soup.find_all('td', class_="Py(10px) Ta(start) Pend(10px)")
prices = soup.find_all('td', class_='Py(10px) Pstart(10px)')

#list to store the days once in correct format
days = []

for dayRaw in daysRaw:
    string = '' + str(dayRaw.find('span').text)
    days.append(string)

#lists which will hold the open price, high price, low price, close price, average, and volume
openPrice = []
high = []
low = []
close = []
average = []
volume = []
totalElements = int(len(prices)/6)
axis = []

#loop which will place value in corresponding list
for x in range(totalElements):
    openPrice.append(float(prices[6*x].find('span').text))
    high.append(float(prices[6*x+1].find('span').text))
    low.append(float(prices[6*x+2].find('span').text))
    close.append(float(prices[6*x+3].find('span').text))
    volumeList = (prices[6*x+5].find('span').text).split(',')
    average.append((openPrice[x] + close[x])/2)
    #change the format of volume to be just an int
    value = ''
    axis.append(x)
    for element in volumeList:
        value = value + element
    volume.append(int(value))

average.reverse()
openPrice.reverse()
high.reverse()
low.reverse()
close.reverse()
volume.reverse()
days.reverse()

#plotting the graph
plt.plot(axis, average, color='black', linewidth=2)
plt.plot(axis, high, color='red', linewidth=1)
plt.plot(axis, low, color='green', linewidth=1)

#label the axis
plt.title("price of " + asset +" over the past 100 working days")
plt.xlabel("days")
plt.ylabel('price $')

#display the graph
#plt.show()

# Function to find the product term
def proterm(i, value, x):
    pro = 1
    for j in range(i):
        pro = pro * (value - x[j])
    return pro

# Function for calculating
# divided difference table
def dividedDiffTable(x, y, n):
    for i in range(1, n):
        for j in range(n - i):
            y[j][i] = ((y[j][i - 1] - y[j + 1][i - 1]) /
                       (x[j] - x[i + j]))
    return y

# Function for applying Newton's
# divided difference formula

def applyFormula(value, x, y, n):
    sum = y[0][0]
    for i in range(1, n):
        sum = sum + (proterm(i, value, x) * y[0][i])
    return sum

# Function for displaying divided
# difference table

# number of inputs given
y = [[0 for i in range(totalElements)]
     for j in range(totalElements)]

# y[][] is used for divided difference
# table where y[][0] is used for input
for i in range(totalElements):
    y[i][0] = average[i]

# calculating divided difference table
y = dividedDiffTable(axis, y, totalElements)

# value to be interpolated
values = []

for i in range(totalElements):
    print('actual ' + str(average[i]))
    print(round(applyFormula(i, axis, y, totalElements), 2))



