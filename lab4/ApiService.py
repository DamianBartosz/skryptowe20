from copy import copy

import requests
from datetime import date, timedelta

url = "http://api.nbp.pl/api/exchangerates/rates/"


class AverageExchangeRate:
    def __init__(self, currencyCode, mid, dateStr, interpolated=False):
        self.currencyCode = currencyCode
        self.mid = mid
        dateStrSplited = dateStr.split("-")
        self.effectiveDate = date(int(dateStrSplited[0]), int(dateStrSplited[1]), int(dateStrSplited[2]))
        self.interpolated = interpolated

    def __str__(self):
        return '{}|{}|{}|{}'.format(self.currencyCode, self.mid, self.effectiveDate, self.interpolated)


def getAverageExchangeRatesInDays(currencyCode, days, tableCode='a', endDate=date.today()):
    days -= 1
    returnData = []
    if days > 366:
        returnData += getAverageExchangeRatesInDays(currencyCode, days - 366, tableCode, endDate - timedelta(days=367))
        days = 366

    resp = __getCurrencyFromOneTableInDays__(tableCode, currencyCode, days, endDate)

    if resp.status_code != 200:
        return []

    for item in resp.json()["rates"]:
        returnData.append(AverageExchangeRate(currencyCode, item["mid"], item["effectiveDate"]))
    return returnData


def __getCurrencyFromOneTableInDays__(tableCode, currencyCode, days, endDate):
    startDate = endDate - timedelta(days=days)

    paramsUrl = "/{}/{}/{}".format(currencyCode, startDate, endDate)
    return requests.get(url + tableCode + paramsUrl)


def getLastAverageExchangeBeforeDate(date, tableCode, currencyCode):
    for i in range(14):
        date -= timedelta(days=1)
        exchange = requests.get(url + '{}/{}/{}'.format(tableCode, currencyCode, date))
        if exchange.status_code == 200:
            return True, exchange.json()['rates'][0]
    return False, 0


def getAverageExchangeRatesInDaysWithoutGaps(currencyCode, days, tableCode='a', endDate=date.today()):
    resultWithGaps = getAverageExchangeRatesInDays(currencyCode, days, tableCode, endDate)
    startDate = endDate - timedelta(days=days - 1)
    if resultWithGaps[0].effectiveDate != startDate:
        found, exchange = getLastAverageExchangeBeforeDate(startDate, tableCode, currencyCode)
        if found:
            resultWithGaps = [AverageExchangeRate(currencyCode, exchange['mid'],
                                                  startDate.strftime('%Y-%m-%d'), True)] + resultWithGaps

    filledList = []
    lastExchange = resultWithGaps[0]
    for ex in resultWithGaps:
        while lastExchange.effectiveDate < ex.effectiveDate:
            filledList.append(copy(lastExchange))
            lastExchange.effectiveDate += timedelta(days=1)
        filledList.append(ex)
        lastExchange = copy(ex)
        lastExchange.effectiveDate += timedelta(days=1)
        lastExchange.interpolated = True
    lastExchange = copy(filledList[len(filledList) - 1])
    lastExchange.interpolated = True
    while lastExchange.effectiveDate < endDate:
        lastExchange.effectiveDate += timedelta(days=1)
        filledList.append(copy(lastExchange))
    return filledList


def getUsdAndEurOverHalfOfYear(endDate=date.today()):
    return getAverageExchangeRatesInDaysWithoutGaps("USD", 182, endDate=endDate), \
           getAverageExchangeRatesInDaysWithoutGaps("EUR", 182, endDate=endDate)
