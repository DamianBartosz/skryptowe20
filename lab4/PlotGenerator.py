import matplotlib.pyplot as plt
from datetime import date
from ApiService import getUsdAndEurOverHalfOfYear
from DatabaseService import getPricesUsdPlnInHalfYear


def generateUsdAndEurOverHalfOfYearPlot():
    usd, eur = getUsdAndEurOverHalfOfYear(date(2018, 5, 6))
    (usdMid, usdDates, eurMid, eurDates) = getUsdAndEurDataLists(usd, eur)

    plt.scatter(
        usdDates, usdMid, c="blue", edgecolor="black", linewidths=1, label="USD"
    )

    plt.scatter(
        eurDates, eurMid, c="red", edgecolor="black", linewidths=1, label="EUR"
    )

    plt.title("Plot of average EUR and USD exchange rates over the last six months")
    plt.xlabel("Date")
    plt.ylabel("Exchange rate")
    plt.legend()
    plt.savefig("UsdAndEurOverHalfOfYear.svg")
    plt.show()


def generateUsdAndPlnPricesOverHalfOfYearPlot():
    (usdPrices, plnPrices, dates) = getUsdAndPlnPricesDataLists(getPricesUsdPlnInHalfYear())

    plt.plot(
        dates, usdPrices, c="blue",  label="USD"
    )

    plt.plot(
        dates, plnPrices, c="red",  label="PLN"
    )

    plt.title("Plot of total sales in PLN and USD over six months")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.savefig("UsdAndPlnInHalfYear.svg")
    plt.show()


def getUsdAndPlnPricesDataLists(data):
    usdPrices = []
    plnPrices = []
    dates = []
    for item in data:
        usdPrices.append(item[1])
        plnPrices.append(item[2])
        dates.append(date(*[int(item) for item in item[0].split('-')]))

    return usdPrices, plnPrices, dates


def getUsdAndEurDataLists(usd, eur):
    usdMid = []
    usdDates = []
    eurMid = []
    eurDates = []
    for u in usd:
        usdMid.append(u.mid)
        usdDates.append(u.effectiveDate)
    for e in eur:
        eurMid.append(e.mid)
        eurDates.append(e.effectiveDate)
    return usdMid, usdDates, eurMid, eurDates


if __name__ == '__main__':
    generateUsdAndEurOverHalfOfYearPlot()
    generateUsdAndPlnPricesOverHalfOfYearPlot()
