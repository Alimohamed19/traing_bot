import requests
from dotenv import load_dotenv
import os

load_dotenv()

# توكن API لـ CoinMarketCap
API_KEY = os.getenv("COINMARKETCAP_API_KEY")


# دالة لجلب بيانات الشموع اليابانية
def FetchOHLCV(symbol, convert='USD', interval='1d', limit=1):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY
    }
    params = {
        'symbol': symbol,
        'convert': convert,
        'interval': interval,
        'count': limit
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'quotes' in data['data']:
            ohlcv = data['data']['quotes'][-1]['quote'][convert]
            high = ohlcv['high']
            low = ohlcv['low']
            close = ohlcv['close']
            return {'high': high, 'low': low, 'close': close}
        else:
            return f"No data found for {symbol}."
    else:
        return f"Error fetching data: {response.status_code}"

# دالة لحساب مستويات الدعم والمقاومة
def Support_denominator(symbol):
    ohlcv = FetchOHLCV(symbol)
    
    if isinstance(ohlcv, dict):
        high = ohlcv['high']
        low = ohlcv['low']
        close = ohlcv['close']
        PP = (high + low + close) / 3
        R1 = (2 * PP) - low
        R2 = (high - low) + PP
        R3 = high + 2 * (PP - low)
        s1 = (2* PP) - high
        s2 = PP - (high -low)
        s3 = low - 2 * (high - PP)
        return{
            "PP": PP,
            "R1": R1,
            "R2": R2,
            "R3": R3,
            "S1": s1,
            "S2": s2,
            "S3": s3
        }
    else:
        return ohlcv

def get_crypto_details(symbol):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {"X-CMC_PRO_API_KEY": API_KEY}
    params = {"symbol": symbol, "convert": "USD"}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()       
        # print(data) 
        if symbol in data["data"]:
            crypto_data = data["data"][symbol]["quote"]["USD"]
            price = crypto_data["price"]
            change_24h = crypto_data["percent_change_24h"]
            market_cap = crypto_data["market_cap"]
            name = data["data"][symbol]["name"]
            best_buy_price = price * 0.98  # فرضنا أن أفضل سعر شراء هو 2% أقل من السعر الحالي
            best_sell_price = price * 1.02  # فرضنا أن أفضل سعر بيع هو 2% أكثر من السعر الحالي
            expected_price_change = abs(price * (change_24h / 100))
            entry_price = price - expected_price_change
            exit_price = price + expected_price_change
            # image_id = data["data"][symbol]["id"]
            # symbol_image = f"https://s2.coinmarketcap.com/static/img/coins/64x64/{data['data'][symbol]['id']}.png"

            # name = data["data"][symbol]["quote"]
            percent_change_1h = crypto_data["percent_change_1h"]
            if percent_change_1h > 0 and change_24h > 0:
                trend = "📉⏫Continuous rise"
            elif percent_change_1h < 0 and change_24h > 0:
                trend = "🔽⬆️ A stalled increase or slight decline"
            elif percent_change_1h > 0 and change_24h < 0:
                trend = "📊↘️↗️ Change the trend to up after down"
            else:
                trend = "📈⏬ Continuous decline"

            #  📊📈📉
            wordsName = name.split()
            NameImg = ""
            for word in wordsName:
                NameImg += "-"+ word
            image_url = f"https://static.coinpaprika.com/coin/{symbol.lower()}{NameImg.lower()}/logo.png"
            SupportDenom = Support_denominator(symbol)
            return {
                "details": (
                    f"💎Name : ({symbol}) {name}\n"
                    f"🔹 Current price: ${f'{price:,.8f}'}\n"
                    f"🔺Change within 24 hours:{f'{change_24h:,.5f}'}%\n"
                    f"💰 Market value: ${f'{market_cap:,.5f}'}\n"
                    f"=======================\n"
                    f" likely expectation: {trend}\n"
                    f"=======================\n"
                    f"Best buy price: ${f'{best_buy_price:,.8f}'}\n"
                    f"Best sell price: ${f'{best_sell_price:,.8f}'}\n"
                    f"=======================\n"
                    f"🔥🔥🔥🔥🔥🔥🔥🔥🔥\n"
                    f"Entry and exit points:\n"
                    f"🔜Entry price: ${entry_price:,.8f}\n"
                    f"🔚Exit price: ${exit_price:,.8f}\n"
                    f"=======================\n"
                    f"Support and denominator points\n"
                    f"Resistance Levels:\n"
                    f"↘️level One:{SupportDenom['R1']:,.8f}\n"
                    f"↘️level Two:{SupportDenom['R2']:,.8f}\n"
                    f"↘️level three:{SupportDenom['R3']:,.8f}\n"
                    f"Support Levels:\n"
                    f"↗️level One:{SupportDenom['S1']:,.8f}\n"
                    f"↗️level Two:{SupportDenom['S2']:,.8f}\n"
                    f"↗️level three:{SupportDenom['S3']:,.8f}\n"
                ),
                "image_url": image_url
            }
        else:
            return "❗️ Currency symbol not found in data."
    else:
        return "❗️ An error occurred while fetching data. Check the currency symbol."
    


def get_top_cryptos(type_):
    try:
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        headers = {"X-CMC_PRO_API_KEY": API_KEY}
        params = {"sort": "percent_change_24h", "convert": "USD"}
        
        if type_ == "losers":
            params["sort_dir"] = "asc"
        # طلب البيانات من API
        response = requests.get(url, headers=headers, params=params)
        
        # التحقق من نجاح الاستجابة
        if response.status_code == 200:
            data = response.json()
            
            if "data" in data:
                top_cryptos = data["data"][:5]
                msg = ""
                
                for crypto in top_cryptos:
                    symbol = crypto["symbol"]
                    try:
                        # محاولة الحصول على تفاصيل العملة
                        details = get_crypto_details(symbol)["details"]
                        msg += f"{details}\n============================\n\n"
                    except Exception as e:
                        # في حالة حدوث خطأ أثناء جلب التفاصيل
                        msg += f"❗️ An error occurred while fetching currency details {symbol}: {str(e)}\n"
                
                return f"📈 Top currencies {type_}:\n===============\n" + msg
            else:
                return "❗️ No currency data found."
        else:
            return f"❗️ An error occurred while fetching data. Response code: {response.status_code}"
    
    except requests.exceptions.RequestException as e:
        return f"❗️An error occurred connecting to the API: {str(e)}"
    
    except KeyError as e:
        return f"❗️ An error occurred while processing data: key not found {str(e)}"
    
    except Exception as e:
        return f"❗️ An unexpected error occurred: {str(e)}"
