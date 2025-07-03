import requests
import json
import os
from dotenv import load_dotenv
from info import FetchOHLCV,Support_denominator

# تحميل مفاتيح البيئة من ملف .env
load_dotenv()

# الحصول على مفاتيح البيئة
COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY")
OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")

# دالة لجلب بيانات العملة من CoinMarketCap
# دالة لجلب بيانات العملة من CoinMarketCap
def fetch_crypto_data(symbol='BTC'):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
    }
    params = {
        'symbol': symbol,
        'convert': 'USD'  # تحويل السعر إلى الدولار الأمريكي
    }

    try:
        # إرسال الطلب إلى API
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # التأكد من عدم وجود خطأ في الاستجابة

        # إعادة البيانات كاملة كـ JSON
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"حدث خطأ أثناء جلب بيانات العملة {symbol}: {str(e)}"}


def data_Evidence_Support( symbol = "BTC" ) :
    # إعداد URL لـ CoinMarketCap API
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    # إعداد العملة المطلوبة
    # إعداد رؤوس الطلب
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY,
    }
    # إرسال الطلب
    params = {"symbol": symbol, "convert": "USD"}
    response = requests.get(url, headers=headers, params=params)
    # التحقق من النجاح
    if response.status_code == 200:
        data = response.json()
        quote = data["data"][symbol]["quote"]["USD"]
        return quote
    else:
        return("❗️Error fetching data:", response.status_code, response.text)

# دالة لتحليل بيانات العملة باستخدام OpenAI API
def analyze_crypto_data(symbol, message, language="ar"):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    # جلب بيانات العملة
    crypto_data = fetch_crypto_data(symbol=symbol)
    Evidence_Support = data_Evidence_Support(symbol=symbol)
    fetchOHLCV = FetchOHLCV(symbol=symbol , convert='USD', interval='1d')
    support_denominator = Support_denominator(symbol=symbol)
    if isinstance(crypto_data, dict):  # التحقق إذا كانت البيانات صحيحة
        content = f"{message} البيانات هي: {crypto_data} و{Evidence_Support} و{fetchOHLCV} و {support_denominator}. الرد يجب أن يكون باللغة {language}. خد البيانات على أنها مرجع لك و متجوبش غير علي الاسئلة المحددة ياعني متزودش علي السؤال ياعني اعرفها كا مرجع زيادة ومش عايزك تقول نعم المعلومات الي بعتها خدها كامرجع موثوق بدون متعتبر اني بعتها ."
        data = {
            "model": "gpt-4",  # اختر الطراز المناسب
            "messages": [{"role": "user", "content": content}]
        }
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(data))
            response.raise_for_status()  # التأكد من أن الاستجابة لا تحتوي على خطأ
            response_data = response.json()
            return response_data["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            return f"حدث خطأ في الاتصال بـ OpenAI API: {str(e)}"
    else:
        return "حدث خطأ في جلب بيانات العملة."


# اختبار الدالة
# result = analyze_crypto_data(symbol="BTC", message="اي التغير الي حصل علي عملة البت كوين خلال شهر", language="ar")
# print(result)