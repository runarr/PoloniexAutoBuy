import io, sys, time, datetime, urllib2, json
from poloniex import Poloniex
from ConfigParser import SafeConfigParser

#get config
config = SafeConfigParser()
config_location = 'default.cfg'
loadedFiles = config.read([config_location])
duration = float(config.get("BOT", "duration"))
frequency = int(config.get("BOT", "frequency"))
total_amount_to_spend = float(config.get("BOT", "totalAmountToSpend"))
api_key = config.get("API","apikey")
api_secret = config.get("API","secret")

currency_pair = "BTC_XMR"

bot = Poloniex(api_key, api_secret)

amount_each_trade = total_amount_to_spend/(duration*3600/frequency)
amount_traded_in_btc = 0.0
amount_xmr_bought = 0.0

def get_buy_price():
    order_book = bot.returnOrderBook(currency_pair)
    asks = order_book["asks"]
    amount = 0.0
    for i, val in enumerate(asks):
        amount += (float(val[0]) * val[1])
        if amount >= amount_each_trade:
            return float(val[0])


while True:
    buy_price = get_buy_price()
    amount_traded_in_btc += amount_each_trade
    xmr_amount_to_buy = amount_each_trade/buy_price
    amount_xmr_bought += xmr_amount_to_buy
    print "---BUYING--- Buy price: ", buy_price, " Total XMR bought: ", amount_xmr_bought, "Total BTC spent: ", amount_traded_in_btc
    print bot.buy(currency_pair, buy_price, xmr_amount_to_buy, 1)

    if (amount_traded_in_btc >= total_amount_to_spend):
        print "Buying completed. Bought ", amount_xmr_bought, " XMR, spent ", amount_traded_in_btc, " BTC"
        break

    time.sleep(frequency)
