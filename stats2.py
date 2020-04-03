import requests
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import sys
import tweepy
import time
import os
import csv
import sys

symbols = []
stockCounter = 0
c = 0

overall = []
outputPrint = []


def clean(stng):
    
    output = ''

    for letter in stng:
        if letter != '[' and letter != ']' and letter != "'": #and letter != ' ':
            output += letter
        
    return output


def progress(count, total, status=''):
    
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


def fixString(stng):
    
    output = ''
    output2 = ''
    
    if '&amp;' in stng:
        output += stng[0 : stng.find('&') + 1]
        output += stng[stng.find(';') + 1 : ]
    else:
        output = stng
    
    for letter in output:
        if letter != ',':
            output2 += letter

    return output2
    

def getSymbols(inURL, numStocks):
    
    global symbols
    global stockCounter
    global c

    page = requests.get(inURL)
    soup = BeautifulSoup(page.text, 'html.parser')
    symbs = soup.find_all('a', {'class' : 'screener-link-primary'})

    for x in range(len(symbs)):
        if '&amp;b=1' in str(symbs[x]):
            symbols.append(str(symbs[x])[str(symbs[x]).find('&amp;b=1') + 10 : str(symbs[x]).find('/a') - 1])
            stockCounter = stockCounter + 1

        if stockCounter % 20 == 0:
            c = c + 20
            getSymbols(inURL + '&r=' + str(c), numStocks)
        
        if stockCounter >= numStocks:
            break


def generateSymbolsCSV(fileName, url, numStocks):

    global symbols

    getSymbols(url, numStocks)

    print('Gathering stock symbols from ' + url)
    saveTo = 'C:\\Users\\faiza\\OneDrive\\Desktop\\StockData\\SymbolData\\' + fileName + '.csv'

    MyFile = open(saveTo, 'w')

    for symbol in symbols:
        MyFile.write(clean(str(symbol)))
        MyFile.write('\n')

    MyFile.close()

    print('\nSaved as ' + saveTo)


def convertNum(stng):
    s = ''

    if len(stng) > 20:
        return 0

    for x in range(len(stng)):
        if x != len(stng) - 1 and stng[x] == '-' and stng[x + 1] != '-':
            s += stng[x]
        
        elif stng[x] == '.':
            s += stng[x]

        elif x != len(stng) - 1 and stng[x] != ',' and stng[x] != "'" and stng[x] != '"' and (not stng[x].isalpha()) and stng[x] != ':' and stng[x].isdigit() and stng[x + 1] != '"':
            s += stng[x]

    if len(s) > 0 and len(s) < 10:
        try:
            return float(s)
        except:
            return 0

    return 0


def convertToLetterGrade(num):
    
    output = 'F'

    if num == 4.3:
        output = 'A+'
    elif num >= 4.0:
        output = 'A'
    elif num >= 3.7:
        output = 'A-'
    elif num >= 3.3:
        output = 'B+'
    elif num >= 3:
        output = 'B'
    elif num >= 2.7:
        output = 'B-'
    elif num >= 2.3:
        output = 'C+'
    elif num >= 2:
        output = 'C'
    elif num >= 1.7:
        output = 'C-'
    elif num >= 1.3:
        output = 'D+'
    elif num >= 1:
        output = 'D'
    elif num >= 0.7:
        output = 'D-'

    return output
    

def getGrade(mtrc, val):

    start = 0
    change = 0
    lessThan = False
    grade = 'F'

    if mtrc == 'forwardPE':
        start = 10
        change = 2.5
        lessThan = True

        if val == 0:
            return 'D'

    if mtrc == 'peg':
        start = 0.70
        change = 0.25
        lessThan = True

        if val == 0:
            return 'D'
    
    if mtrc == 'priceSales':
        start = 3
        change = 1.5
        lessThan = True

        if val == 0:
            return 'D'

    if mtrc == 'priceBook':
        start = 3.5
        change = 1.5
        lessThan = True

        if val == 0:
            return 'D'

    if mtrc == 'priceFCF':
        start = 15
        change = 5
        lessThan = True

        if val == 0: 
            return 'D'

    if mtrc == 'profitMargin':
        start = 30
        change = 4

        if val == 0:
            return 'C'

    if mtrc == 'operMargin':
        start = 35
        change = 4

        if val == 0:
            return 'C'

    if mtrc == 'grossMargin':
        start = 40
        change = 4

        if val == 0:
            return 'B'

    if mtrc == 'roe':
        start = 30
        change = 4

        if val == 0:
            return 'D'

    if mtrc == 'roa':
        start = 15
        change = 3.5

        if val == 0:
            return 'D'

    if mtrc == 'epsThisY':
        start = 30
        change = 4

        if val == 0:
            return 'F'

    if mtrc == 'epsNextY':
        start = 25
        change = 3.5

        if val == 0:
            return 'F'

    if mtrc == 'epsNext5Y':
        start = 15
        change = 3.5

        if val == 0:
            return 'C'

    if mtrc == 'salesQQ':
        start = 10 
        change = 2.5

        if val == 0:
            return 'D'

    if mtrc == 'epsQQ':
        start = 10
        change = 2.5

        if val == 0:
            return 'D'

    if mtrc == 'perfMonth':
        start = 5
        change = 2.5

        if val == 0:
            return 'C'

    if mtrc == 'perfQuarter':
        start = 8
        change = 3

        if val == 0:
            return 'C'

    if mtrc == 'perfHalfY':
        start = 10
        change = 3

        if val == 0:
            return 'D'

    if mtrc == 'perfYear':
        start = 15
        change = 3.5

        if val == 0:
            return 'F'

    if mtrc == 'perfYTD':
        start = 10
        change = 3

        if val == 0:
            return 'F'

    if mtrc == 'volatility':
        start = 3.00
        change = 0.40
        lessThan = True

        if val > 9.5:
            return 'F-'


    if lessThan == True:

        if val < start:
            grade = 'A+'
        elif val < start + change:
            grade = 'A'
        elif val < start + (change * 2):
            grade = 'A-'
        elif val < start + (change * 3):
            grade = 'B+'
        elif val < start + (change * 4):
            grade = 'B'
        elif val < start + (change * 5):
            grade = 'B-'
        elif val < start + (change * 6):
            grade = 'C+'
        elif val < start + (change * 7):
            grade = 'C'
        elif val < start + (change * 8):
            grade = 'C-'
        elif val < start + (change * 9):
            grade = 'D+'
        elif val < start + (change * 10):
            grade = 'D'
        elif val < start + (change * 11):
            grade = 'D-'

    else:

        if val > start:
            grade = 'A+'
        elif val > start - change:
            grade = 'A'
        elif val > start - (change * 2):
            grade = 'A-'
        elif val > start - (change * 3):
            grade = 'B+'
        elif val > start - (change * 4):
            grade = 'B'
        elif val > start - (change * 5):
            grade = 'B-'
        elif val > start - (change * 6):
            grade = 'C+'
        elif val > start - (change * 7):
            grade = 'C'
        elif val > start - (change * 8):
            grade = 'C-'
        elif val > start - (change * 9):
            grade = 'D+'
        elif val > start - (change * 10):
            grade = 'D'
        elif val > start - (change * 11):
            grade = 'D-'


    return grade


def getCategoryGrade(arr):
    score = 0
    grade = "F"
    output = []

    for x in range(len(arr)):
        output.append(getGrade(arr[x][0], arr[x][1]))

    for grade in output:

        if grade == 'A+':
            score += 4.3
        if grade == 'A':
            score += 4
        if grade == 'A-':
            score += 3.7
        if grade == 'B+':
            score += 3.3
        if grade == 'B':
            score += 3
        if grade == 'B-':
            score += 2.7
        if grade == 'C+':
            score += 2.3
        if grade == 'C':
            score += 2 
        if grade == 'C-':
            score += 1.7
        if grade == 'D+':
            score += 1.3
        if grade == 'D':
            score += 1
        if grade == 'D-':
            score += 0.7
        if grade == 'F-':
            score -= 1.5

    #print(output)
    return score / len(arr)


def getOverallRating(valGrade, profGrade, grGrade, pfGrade, vol):

    if vol > 2.1:
        return ((valGrade * 1.05) + profGrade + grGrade + pfGrade) * 6.25
    
    return ((valGrade * 1.20) + profGrade + grGrade + pfGrade) * 6.25  


def getRating(sym, val, prof, growth, perf):

    score = 0
    overallStats = []
    overallStats.append(getCategoryGrade(val))
    overallStats.append(getCategoryGrade(prof))
    overallStats.append(getCategoryGrade(growth))
    overallStats.append(getCategoryGrade(perf))

    '''
    print('Valuation:', getValuationGrade(val))
    print('Profitability:', getProfitabilityGrade(prof))
    print('Growth:', getGrowthGrade(growth))
    print('Performance:', getPerfGrade(perf))
    '''

    for grade in overallStats:
        
        if grade == 'A+':
            score += 4.3
        if grade == 'A':
            score += 4
        if grade == 'A-':
            score += 3.7
        if grade == 'B+':
            score += 3.3
        if grade == 'B':
            score += 3
        if grade == 'B-':
            score += 2.7
        if grade == 'C+':
            score += 2.3
        if grade == 'C':
            score += 2 
        if grade == 'C-':
            score += 1.7
        if grade == 'D+':
            score += 1.3
        if grade == 'D':
            score += 1
        if grade == 'D-':
            score += 0.7

    score = ((score * 25) / 4) + 6
    
    #print(score)
    #print()
    return score


def getInfo(sym):

    global overall

    page = requests.get('https://finviz.com/quote.ashx?t=' + sym)
    soup2 = BeautifulSoup(page.text, 'html.parser')
    soup = str(BeautifulSoup(page.text, 'html.parser'))

    valuationStats = []
    profitabilityStats = []
    growthStats = []
    perfStats = []

    rawMarketCap = soup[soup.find('Market capitalization') : soup.find('Market capitalization') + 200]
    marketCap = rawMarketCap[rawMarketCap.find('<b>') + 3 : rawMarketCap.find('</b>')]

    rawCompanyName = soup[soup.find('id="ticker">') + 100 : soup.find('id="ticker">') + 500]
    companyName = rawCompanyName[rawCompanyName.find('<b>') + 3 : rawCompanyName.find('</b>')]

    rawSector = rawCompanyName[rawCompanyName.find('f=sec') : rawCompanyName.find('f=sec') + 50]
    sector = rawSector[rawSector.find('>') + 1 : rawSector.find('</a>')]

    rawIndustry = rawCompanyName[rawCompanyName.find('f=ind') : rawCompanyName.find('f=ind') + 100]
    industry = rawIndustry[rawIndustry.find('>') + 1 : rawIndustry.find('</a>')]

    ##Valuation

    rawforwardPE = soup[soup.find('Forward P/E') : soup.find('Forward P/E') + 150]
    forwardPE = convertNum(rawforwardPE[rawforwardPE.find('<b>') + 3 : rawforwardPE.find('</b>') + 1])

    if forwardPE == 0:
        forwardPE = convertNum(rawforwardPE[rawforwardPE.find(';') + 3 : rawforwardPE.find('</span>') + 1])

    rawPEG = soup[soup.find('PEG') : soup.find('PEG') + 150]
    peg = convertNum(rawPEG[rawPEG.find('<b>') + 3 : rawPEG.find('</b>') + 1])

    if peg == 0:
        peg = convertNum(rawPEG[rawPEG.find(';') + 3 : rawPEG.find('</span>') + 1])

    rawPriceSales = soup[soup.find('P/S') : soup.find('P/S') + 150]
    priceSales = convertNum(rawPriceSales[rawPriceSales.find('<b>') + 3 : rawPriceSales.find('</b>') + 1])

    if priceSales == 0:
        priceSales = convertNum(rawPriceSales[rawPriceSales.find(';') + 3 : rawPriceSales.find('</span>') + 1])

    rawPriceBook = soup[soup.find('P/B') : soup.find('P/B') + 150]
    priceBook = convertNum(rawPriceBook[rawPriceBook.find(';') + 3 : rawPriceBook.find('</span>') + 1])

    if priceBook == 0:
        priceBook = convertNum(rawPriceBook[rawPriceBook.find('<b>') + 3 : rawPriceBook.find('</b>') + 1])

    rawPriceFCF = soup[soup.find('P/FCF') : soup.find('P/FCF') + 150]
    priceFCF = convertNum(rawPriceFCF[rawPriceFCF.find('<b>') + 3 : rawPriceFCF.find('</b>') + 1])

    if priceFCF == 0:
        priceFCF = convertNum(rawPriceFCF[rawPriceFCF.find(';') + 3 : rawPriceFCF.find('</span>') + 1])

    #print(sym)
    valuationStats.append(['forwardPE', forwardPE])
    valuationStats.append(['peg', peg])
    valuationStats.append(['priceSales', priceSales])
    valuationStats.append(['priceBook', priceBook])
    valuationStats.append(['priceFCF', priceFCF])
    valuationGrade = getCategoryGrade(valuationStats)
    
    #print('Valuation Grade:', valuationGrade, convertToLetterGrade(valuationGrade))


    ##Profitability

    rawProfitMargin = soup[soup.find('Profit Margin') : soup.find('Profit Margin') + 250]
    profitMargin = convertNum(rawProfitMargin[rawProfitMargin.find(';') + 3 : rawProfitMargin.find('</span>') + 1])
   
    if profitMargin == 0:
        profitMargin = convertNum(rawProfitMargin[rawProfitMargin.find('<b>') + 3 : rawProfitMargin.find('</b>') + 1])

    rawOperMargin = soup[soup.find('Operating Margin') : soup.find('Operating Margin') + 250]
    operMargin = convertNum(rawOperMargin[rawOperMargin.find(';') + 3 : rawOperMargin.find('</span>') + 1])
   
    if operMargin == 0:
        operMargin = convertNum(rawOperMargin[rawOperMargin.find('<b>') + 3 : rawOperMargin.find('</b>') + 1])

    rawGrossMargin = soup[soup.find('Gross Margin') : soup.find('Gross Margin') + 250]
    grossMargin = convertNum(rawGrossMargin[rawGrossMargin.find('<b>') + 3 : rawGrossMargin.find('</b>') + 1])

    if grossMargin == 0:
        grossMargin = convertNum(rawGrossMargin[rawGrossMargin.find(';') + 3 : rawGrossMargin.find('</span>') + 1])

    rawROE = soup[soup.find('ROE') : soup.find('ROE') + 250]
    roe = convertNum(rawROE[rawROE.find(';') + 3 : rawROE.find('</span>') + 1])

    if roe == 0:
        roe = convertNum(rawROE[rawROE.find('<b>') + 3 : rawROE.find('</b>') + 1])

    rawROA = soup[soup.find('ROA') : soup.find('ROA') + 250]
    roa = convertNum(rawROA[rawROA.find(';') + 3 : rawROA.find('</span>') + 1])
    
    if roa == 0:
        roa = convertNum(rawROA[rawROA.find('<b>') + 3 : rawROA.find('</b>') + 1])
    
    profitabilityStats.append(['profitMargin', profitMargin])
    profitabilityStats.append(['operMargin', operMargin])
    profitabilityStats.append(['grossMargin', grossMargin])
    profitabilityStats.append(['roe', roe])
    profitabilityStats.append(['roa', roa])
    
    profitabilityGrade = getCategoryGrade(profitabilityStats)
    #print('Profitability Grade:', profitabilityGrade, convertToLetterGrade(profitabilityGrade))


    ##Growth

    rawEPSThisY = soup[soup.find('EPS this Y') : soup.find('EPS this Y') + 250]
    epsThisY = convertNum(rawEPSThisY[rawEPSThisY.find(';') + 3 : rawEPSThisY.find('</span>') + 1])

    if epsThisY == 0:
        epsThisY = convertNum(rawEPSThisY[rawEPSThisY.find('<b>') + 3 : rawEPSThisY.find('</b>') + 1])

    rawEPSNextY = soup[soup.find('EPS growth next year') : soup.find('EPS growth next year') + 250]
    epsNextY = convertNum(rawEPSNextY[rawEPSNextY.find('<b>') + 3 : rawEPSNextY.find('</b>') + 1])

    if epsNextY == 0:
        epsNextY = convertNum(rawEPSNextY[rawEPSNextY.find(';') + 3 : rawEPSNextY.find('</span>') + 1])

    rawEPSNext5Y = soup[soup.find('EPS next 5Y') : soup.find('EPS next 5Y') + 250]
    epsNext5Y = convertNum(rawEPSNext5Y[rawEPSNext5Y.find('<b>') + 3 : rawEPSNext5Y.find('</b>') + 1])

    if epsNext5Y == 0:
        epsNext5Y = convertNum(rawEPSNext5Y[rawEPSNext5Y.find(';') + 3 : rawEPSNext5Y.find('</span>') + 1])

    rawSalesQQ = soup[soup.find('Sales Q/Q') : soup.find('Sales Q/Q') + 250]
    salesQQ = convertNum(rawSalesQQ[rawSalesQQ.find(';') + 3 : rawSalesQQ.find('</span>') + 1])

    if salesQQ == 0:
        salesQQ = convertNum(rawSalesQQ[rawSalesQQ.find('<b>') + 3 : rawSalesQQ.find('</b>') + 1])

    rawEPSQQ = soup[soup.find('EPS Q/Q') : soup.find('EPS Q/Q') + 250]
    epsQQ = convertNum(rawEPSQQ[rawEPSQQ.find(';') + 3 : rawEPSQQ.find('</span>') + 1])

    if epsQQ == 0:
        epsQQ = convertNum(rawEPSQQ[rawEPSQQ.find('<b>') + 3 : rawEPSQQ.find('</b>') + 1])

    growthStats.append(['epsThisY', epsThisY])
    growthStats.append(['epsNextY', epsNextY])
    growthStats.append(['epsNext5Y', epsNext5Y])
    growthStats.append(['salesQQ', salesQQ])
    growthStats.append(['epsQQ', epsQQ])
    
    growthGrade = getCategoryGrade(growthStats)
    #print('Growth Grade:', growthGrade, convertToLetterGrade(growthGrade))


    ##Performance

    rawPerfMonth = soup[soup.find('Perf Month') : soup.find('Perf Month') + 250]
    perfMonth = convertNum(rawPerfMonth[rawPerfMonth.find(';') + 3 : rawPerfMonth.find('</span>') + 1])

    if perfMonth == 0:
        perfMonth = convertNum(rawPerfMonth[rawPerfMonth.find('<b>') + 3 : rawPerfMonth.find('</b>') + 1])

    rawPerfQuarter = soup[soup.find('Perf Quarter') : soup.find('Perf Quarter') + 250]
    perfQuarter = convertNum(rawPerfQuarter[rawPerfQuarter.find(';') + 3 : rawPerfQuarter.find('</span>') + 1])

    if perfQuarter == 0:
        perfQuarter = convertNum(rawPerfQuarter[rawPerfQuarter.find('<b>') + 3 : rawPerfQuarter.find('</b>') + 1])

    rawPerfHalfY = soup[soup.find('Perf Half Y') : soup.find('Perf Half Y') + 250]
    perfHalfY = convertNum(rawPerfHalfY[rawPerfHalfY.find(';') + 3 : rawPerfHalfY.find('</span>') + 1])

    if perfHalfY == 0:
        perfHalfY = convertNum(rawPerfHalfY[rawPerfHalfY.find('<b>') + 3 : rawPerfHalfY.find('</b>') + 1])

    rawPerfYear = soup[soup.find('Perf Year') : soup.find('Perf Year') + 250]
    perfYear = convertNum(rawPerfYear[rawPerfYear.find(';') + 3 : rawPerfYear.find('</span>') + 1])

    if perfYear == 0:
        perfYear = convertNum(rawPerfYear[rawPerfYear.find('<b>') + 3 : rawPerfYear.find('</b>') + 1])

    rawPerfYTD = soup[soup.find('Perf YTD') : soup.find('Perf YTD') + 250]
    perfYTD = convertNum(rawPerfYTD[rawPerfYTD.find(';') + 3 : rawPerfYTD.find('</span>') + 1])

    if perfYTD == 0:
        perfYTD = convertNum(rawPerfYTD[rawPerfYTD.find('<b>') + 3 : rawPerfYTD.find('</b>') + 1])

    rawVolatility = soup[soup.find('Volatility') : soup.find('Volatility') + 250]
    rawVol = rawVolatility[rawVolatility.find('<small>') + 7 : rawVolatility.find('</small>') + 1]
    volatility = convertNum(rawVol[rawVol.find(' ') + 1 : len(rawVol)])

    if volatility == 0:
        volatility = convertNum(rawVolatility[rawVolatility.find('<b>') + 3 : rawVolatility.find('</b>') + 1])
    
    perfStats.append(['perfMonth', perfMonth])
    perfStats.append(['perfQuarter', perfQuarter])
    perfStats.append(['perfHalfY', perfHalfY])
    perfStats.append(['perfYear', perfYear])
    perfStats.append(['perfYTD', perfYTD])
    perfStats.append(['volatility', volatility])
    
    perfGrade = getCategoryGrade(perfStats)
    #print('Performance Grade:', perfGrade, convertToLetterGrade(perfGrade))
    #print(getGrade('volatility', volatility), volatility)
    
    
    rawDividend = soup[soup.find('Dividend %') : soup.find('Dividend %') + 250]
    dividend = convertNum(rawDividend[rawDividend.find('"><b>') + 5 : rawDividend.find('%</b></td>')])

    if dividend == 0:
        dividend = convertNum(rawDividend[rawDividend.find(';') + 3 : rawDividend.find('</span>') + 1])

    rawSMA20 = soup[soup.find('SMA20') : soup.find('SMA20') + 250]
    sma20 = convertNum(rawSMA20[rawSMA20.find(';">') + 3 : rawSMA20.find('</span></b></td>') - 1])
    
    if sma20 == 0:
        sma20 = convertNum(rawSMA20[rawSMA20.find('<b>') + 3 : rawSMA20.find('</b>') + 1])

    rawSMA50 = soup[soup.find('SMA50') : soup.find('SMA50') + 250]
    sma50 = convertNum(rawSMA50[rawSMA50.find(';">') + 3 : rawSMA50.find('</span></b></td>') - 1])

    if sma50 == 0:
        sma50 = convertNum(rawSMA50[rawSMA50.find('<b>') + 3 : rawSMA50.find('</b>') + 1])

    rawSMA200 = soup[soup.find('SMA200') : soup.find('SMA200') + 250]
    sma200 = convertNum(rawSMA200[rawSMA200.find(';">') + 3 : rawSMA200.find('</span></b></td>') - 1])

    if sma200 == 0:
        sma200 = convertNum(rawSMA200[rawSMA200.find('<b>') + 3 : rawSMA200.find('</b>') + 1])

    rawInstTrans = soup[soup.find('Inst Trans') : soup.find('Inst Trans') + 250]
    instTrans = convertNum(rawInstTrans[rawInstTrans.find('%"><b>') + 3 : rawInstTrans.find('</b></td>')])

    if instTrans == 0:
        instTrans = convertNum(rawInstTrans[rawInstTrans.find(';') + 3 : rawInstTrans.find('</span>') + 1])

    rawInstOwn = soup[soup.find('Inst Own') : soup.find('Inst Own') + 250]
    instOwn = convertNum(rawInstOwn[rawInstOwn.find('%"><b>') + 3 : rawInstOwn.find('</b></td>')])

    if instOwn == 0:
        instOwn = convertNum(rawInstOwn[rawInstOwn.find(';') + 3 : rawInstOwn.find('</span>') + 1])

    rawInsiderOwn = soup[soup.find('Insider Own') : soup.find('Insider Own') + 250]
    insiderOwn = convertNum(rawInsiderOwn[rawInsiderOwn.find('%"><b>') + 3 : rawInsiderOwn.find('</b></td>')])

    if insiderOwn == 0:
        insiderOwn = convertNum(rawInsiderOwn[rawInsiderOwn.find(';') + 3 : rawInsiderOwn.find('</span>') + 1])

    rawInsiderTrans = soup[soup.find('Insider Trans') : soup.find('Insider Trans') + 250]
    insiderTrans = convertNum(rawInsiderTrans[rawInsiderTrans.find('%"><b>') + 3 : rawInsiderTrans.find('</b></td>')])

    if insiderTrans == 0:
        insiderTrans = convertNum(rawInsiderTrans[rawInsiderTrans.find(';') + 3 : rawInsiderTrans.find('</span>') + 1])

    rawTargetPrice = soup[soup.find('Target Price') : soup.find('Target Price') + 250]
    targetPrice = convertNum(rawTargetPrice[rawTargetPrice.find(';">') + 3 : rawTargetPrice.find('</span></b>')])

    if targetPrice == 0:
        targetPrice = convertNum(rawTargetPrice[rawTargetPrice.find('<b>') + 3 : rawTargetPrice.find('</b>') + 1])
    
    rawPrevClose = soup[soup.find('Prev Close') : soup.find('Prev Close') + 250]
    prevClose = convertNum(rawPrevClose[rawPrevClose.find('%"><b>') + 3 : rawPrevClose.find('</b></td>')])

    if prevClose == 0:
        prevClose = convertNum(rawPrevClose[rawPrevClose.find(';') + 3 : rawPrevClose.find('</span>') + 1])

    try:
        priceProjection = (targetPrice - prevClose) / prevClose * 100
    except:
        priceProjection = 0
    
    rawRSI = soup[soup.find('RSI (14)') : soup.find('RSI (14)') + 250]
    RSI = convertNum(rawRSI[rawRSI.find(';">') + 3 : rawRSI.find('</span></b>')])

    if RSI == 0:
        RSI = convertNum(rawRSI[rawRSI.find('<b>') + 3 : rawRSI.find('</b></td>')])
    
    rawShortFloat = soup[soup.find('Short Float') : soup.find('Short Float') + 250]
    shortFloat = convertNum(rawShortFloat[rawShortFloat.find('%"><b>') + 3 : rawShortFloat.find('</b></td>')])

    if shortFloat == 0:
        shortFloat = convertNum(rawShortFloat[rawShortFloat.find(';') + 3 : rawShortFloat.find('</span>') + 1])
    
    raw52WHigh = soup[soup.find('52W High') : soup.find('52W High') + 250]
    fifty2WeekHigh = convertNum(raw52WHigh[raw52WHigh.find('%"><b>') + 3 : raw52WHigh.find('</b></td>')])

    if fifty2WeekHigh == 0:
        fifty2WeekHigh = convertNum(raw52WHigh[raw52WHigh.find(';') + 3 : raw52WHigh.find('</span>') + 1])

    raw52WLow = soup[soup.find('52W Low') : soup.find('52W Low') + 250]
    fifty2WeekLow = convertNum(raw52WLow[raw52WLow.find('%"><b>') + 3 : raw52WLow.find('</b></td>')])

    if fifty2WeekLow == 0:
        fifty2WeekLow = convertNum(raw52WLow[raw52WLow.find(';') + 3 : raw52WLow.find('</span>') + 1])


    rawCurrRatio = soup[soup.find('Current Ratio') : soup.find('Current Ratio') + 250]
    currRatio = convertNum(rawCurrRatio[rawCurrRatio.find(';">') + 3 : rawCurrRatio.find('</span></b>')])

    if currRatio == 0:
        currRatio = convertNum(rawCurrRatio[rawCurrRatio.find('<b>') + 3 : rawCurrRatio.find('</b></td>')])

    rawEarningsDate = soup[soup.find('Earnings date&lt;br&gt') + 150: soup.find('Earnings date&lt;br&gt') + 300]
    earningsDate = rawEarningsDate[rawEarningsDate.find('<b>') + 3 : rawEarningsDate.find('</b></td>')]


    #overallRating = ((valuationGrade * 1.10) + profitabilityGrade + growthGrade + perfGrade) * 6.25 * 1.10 
    overallRating = getOverallRating(valuationGrade, profitabilityGrade, growthGrade, perfGrade, volatility)

    #print('Overall Rating:', overallRating)
    #print()
    
    if overallRating >= 100:
        overallRating = 99

    if len(fixString(companyName)) > 2 and len(marketCap) > 2:
        overall.append([sym, fixString(companyName), marketCap, round(overallRating), 
        fixString(sector), fixString(industry), convertToLetterGrade(getCategoryGrade(valuationStats)), 
        convertToLetterGrade(getCategoryGrade(profitabilityStats)), convertToLetterGrade(getCategoryGrade(growthStats)), 
        convertToLetterGrade(getCategoryGrade(perfStats)), forwardPE, peg, priceSales, priceBook, priceFCF, profitMargin, 
        operMargin, grossMargin, roe, roa, epsThisY, epsNextY, epsNext5Y, salesQQ, epsQQ, perfMonth, perfQuarter, perfHalfY, 
        perfYTD, perfYear, sma20, sma50, sma200, dividend, instTrans, instOwn, insiderOwn, insiderTrans, targetPrice, prevClose, 
        priceProjection, RSI, shortFloat, fifty2WeekHigh, fifty2WeekLow, currRatio, earningsDate])


def getSymbols2():
    
    global symbols

    with open('C:\\Users\\faiza\\OneDrive\\Desktop\\StockData\\StockSharpe\\StockSharpeRatios.csv') as csvfile:
    
        readCSV = csv.reader(csvfile, delimiter=',')
        
        for row in readCSV:
            symbol = row[0]

            if 'Symbol' not in symbol:
                symbols.append(symbol)

        print(symbols)


def getSymbolsCSV(fileName):
    
    global symbols

    with open(fileName) as csvfile:
    
        readCSV = csv.reader(csvfile, delimiter=',')
        
        for row in readCSV:
            if row[0] =='ï»¿A':
                symbols.append('A')
            else:
                symbols.append(row[0])

    print('\nGathering data from ' + fileName)


def getStockStats():

    global symbols

    counter = 0

    for stock in symbols:
    
        getInfo(stock)
        counter += 1
        progress(counter, len(symbols), status='Loading...')


def exportData(fileName):

    MyFile = open(fileName, 'w')

    header = 'Symbol, Company Name, Market Cap, Overall Rating, Sector, Industry, Valuation Grade, Profitability Grade, Growth Grade, Performance Grade, Forward PE, PEG, Price/Sales, Price/Book, Price/FCF, Net Margin, Operating Margin, Gross Margin, ROE, ROA, EPS This Y, EPS Next Y, EPS Next 5 Years, Sales Q/Q, EPS Q/Q, Perf Month, Perf Quarter, Perf Half Y, Perf YTD, Perf Year, SMA20, SMA50, SMA200, Dividend Yield, Inst Trans, Inst Own, Insider Own, Insider Trans, Target Price, Prev Close, Price Projection, RSI, Short Float, 52W High, 52W Low, Current Ratio, Earnings Date' + '\n'

    MyFile.write(header)

    for row in overall:
        MyFile.write(clean(str(row)))
        MyFile.write('\n')

    MyFile.close()

    print('\nSaved as ' + fileName)



sAndP = 'https://finviz.com/screener.ashx?v=111&f=idx_sp500'
midCap = 'https://finviz.com/screener.ashx?v=111&f=cap_mid'
smallCap = 'https://finviz.com/screener.ashx?v=111&f=cap_small'
microCap = 'https://finviz.com/screener.ashx?v=111&f=cap_micro'

basicMaterials = 'https://finviz.com/screener.ashx?v=111&f=sec_basicmaterials'
conglomerates = 'https://finviz.com/screener.ashx?v=111&f=sec_conglomerates'
comsumerGoods = 'https://finviz.com/screener.ashx?v=111&f=sec_consumergoods'
financials = 'https://finviz.com/screener.ashx?v=111&f=sec_financial'
healthcare = 'https://finviz.com/screener.ashx?v=111&f=sec_healthcare'
industrialGoods = 'https://finviz.com/screener.ashx?v=111&f=sec_industrialgoods'
services = 'https://finviz.com/screener.ashx?v=111&f=sec_services'
tech = 'https://finviz.com/screener.ashx?v=111&f=sec_technology'
utilities = 'https://finviz.com/screener.ashx?v=111&f=sec_utilities'

allStocks = 'https://finviz.com/screener.ashx?v=111'



#generateSymbolsCSV('TechSymbols', tech, 100)



searchThrough = 'S&P500'

symbolsFileName = 'C:\\Users\\faiza\\OneDrive\\Desktop\\StockData\\SymbolData\\' + searchThrough + 'Symbols.csv'
saveToFileName = 'C:\\Users\\faiza\\OneDrive\\Desktop\\StockData\\Stats2Outputs\\' + searchThrough + 'Stats2Output.csv'


getSymbolsCSV(symbolsFileName)

getStockStats()

exportData(saveToFileName)

