from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import os

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


def get_currency_trend():
    browser = setup()
    browser.get("https://fx.minkabu.jp/pair/EURJPY")

    html = browser.page_source.encode('utf-8')

    soup = BeautifulSoup(html, "html.parser")

    result = soup.select_one("body > div.l-contents.mt10 > main > div.pairbox > div:nth-child(2) > div > div.pairbox__rate > span.pairbox__rate__item")
    return "💰 " + result.get_text() + " yen/1euro"


def get_appartements_info():
    browser = setup()
    browser.get("https://www.bienici.com/recherche/location/tours-37000/2-pieces-et-plus?mode=carte")
    
    html = browser.page_source.encode('utf-8')
    
    soup = BeautifulSoup(html, "html.parser")
    
    result = ""
    raw_text2 = ""
    page = soup.find_all("div",class_="mainPageContainer")
    for data in page:
        raw_text1 = data.get_text().split("Créer")[:-1]
        raw_text2 = ",".join(raw_text1).split("Appartement")

    for line in raw_text2:
        print("line: ", line)
        if ("€par mois" in line):
            result = result + '\n' + '🏠' + line + '\n' + "-----------"

    browser.close()
    return result


if __name__ == "__main__":
    get_currency_trend()
    get_appartements_info()

