import sqlite3
from datetime import date
from ApiService import getAverageExchangeRatesInDaysWithoutGaps


def getPricesUsdPlnInHalfYear():
    dbConnection = sqlite3.connect("nwdatabase.db")
    dbCursor = dbConnection.cursor()
    dbCursor.execute('''SELECT 
                    RateDate,
                    sales,
                    sales*exchange
                    FROM DailyOrders JOIN ExchangeUsdPln ON RateDate=date
                    WHERE RateDate>="2017-11-05"''')
    result = dbCursor.fetchall()
    dbConnection.close()
    return result


def dropExchangeTable(dbCursor):
    dbCursor.execute('DROP TABLE IF EXISTS ExchangeUsdPln')


def createExchangeTable(dbCursor):
    dbCursor.execute('''
        CREATE TABLE IF NOT EXISTS ExchangeUsdPln(
            RateId INTEGER PRIMARY KEY ASC,
            RateDate DATETIME NOT NULL,
            exchange REAL NOT NULL
        )''')


def fillExchangeTable(dbCursor):
    exchangeRates = getAverageExchangeRatesInDaysWithoutGaps('USD', 672, endDate=date(2018, 5, 6))
    for item in exchangeRates:
        dbCursor.execute('INSERT INTO ExchangeUsdPln VALUES(NULL, ?,?)', (item.effectiveDate, item.mid))


def select(dbCursor):
    dbCursor.execute("Select * from 'Order Details'")
