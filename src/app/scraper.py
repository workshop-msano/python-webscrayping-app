from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import os, math

def setup():

    service = Service(executable_path='/opt/chromedriver')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = "/opt/chrome/chrome"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument("--single-process")
    # chrome_options.add_argument("window-size=2560x1440")
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")
    chrome_options.add_argument("--remote-debugging-port=9222")
    #chrome_options.add_argument("--data-path=/tmp/chrome-user-data")
    #chrome_options.add_argument("--disk-cache-dir=/tmp/chrome-user-data")

    #ブラウザの定義
    browser = webdriver.Chrome(
        service=service,
        options=chrome_options
    )
    return browser

def convert_fahrenheit_to_celsius(num):
    return math.floor((num-32)*5/9)

def get_weather_info():
    browser = setup()
    browser.get(os.environ['WEATHER_URL'])

    html = browser.page_source.encode('utf-8')

    soup = BeautifulSoup(html, "html.parser")

    weather = soup.select_one("#WxuCurrentConditions-main-eb4b02cb-917b-45ec-97ec-d4eb947f6b6a > div > section > div > div > div.CurrentConditions--body--l_4-Z > div.CurrentConditions--columns--30npQ > div.CurrentConditions--primary--2DOqs > div.CurrentConditions--phraseValue--mZC_p")
    day_temp = soup.select_one("#WxuCurrentConditions-main-eb4b02cb-917b-45ec-97ec-d4eb947f6b6a > div > section > div > div > div.CurrentConditions--body--l_4-Z > div.CurrentConditions--columns--30npQ > div.CurrentConditions--primary--2DOqs > div.CurrentConditions--tempHiLoValue--3T1DG > span:nth-child(1)")
    day_temp = convert_fahrenheit_to_celsius(int(day_temp.get_text()[:-1]))
    night_temp = soup.select_one("#WxuCurrentConditions-main-eb4b02cb-917b-45ec-97ec-d4eb947f6b6a > div > section > div > div > div.CurrentConditions--body--l_4-Z > div.CurrentConditions--columns--30npQ > div.CurrentConditions--primary--2DOqs > div.CurrentConditions--tempHiLoValue--3T1DG > span:nth-child(2)")
    night_temp = convert_fahrenheit_to_celsius(int(night_temp.get_text()[:-1]))
    uv_index = soup.select_one("#todayDetails > section > div > div.TodayDetailsCard--detailsContainer--2yLtL > div:nth-child(6) > div.WeatherDetailsListItem--wxData--kK35q > span")
    return f"🌍 Today's weather\n\n{weather.get_text()}. \nDay {day_temp}°/Night {night_temp}°\nUV index: {uv_index.get_text()}"


def get_currency_trend():
    browser = setup()
    browser.get(os.environ['CURRENCY_URL'])
    html = browser.page_source.encode('utf-8')

    soup = BeautifulSoup(html, "html.parser")

    result = soup.select_one("body > div.l-contents.mt10 > main > div.pairbox > div:nth-child(2) > div > div.pairbox__rate > span.pairbox__rate__item")
    return f"💰 {result.get_text()} yen to 1 euro"


def get_appartements_info():
    browser = setup()
    browser.get(os.environ['APARTMENTS_URL'])
    
    html = browser.page_source.encode('utf-8')
    
    soup = BeautifulSoup(html, "html.parser")
    
    result = ""
    raw_text2 = ""
    page = soup.find_all("div",class_="mainPageContainer")
    for data in page:
        raw_text1 = data.get_text().split("Créer")[:-1]
        raw_text2 = ",".join(raw_text1).split("Appartement")

    for line in raw_text2:
        # print("line: ", line)
        if ("€par mois" in line):
            result = result + '\n' + '🏠' + line + '\n' + "-----------"

    browser.close()
    return result


if __name__ == "__main__":
    get_currency_trend()
    get_appartements_info()
    get_weather_info()

