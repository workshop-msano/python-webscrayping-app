from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import os

def setup():

    service = Service(executable_path='/opt/chromedriver')

    options = webdriver.ChromeOptions()
    options.binary_location = "/opt/chrome/chrome"
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--single-process")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--no-sandbox")
    options.add_argument("--homedir=/tmp")

    #ブラウザの定義
    browser = webdriver.Chrome(
        service=service,
        options=options
    )
    return browser


def get_currency_trend():
    browser = setup()
    browser.get(os.environ["CURRENCY_URL"])

    html = browser.page_source.encode('utf-8')

    soup = BeautifulSoup(html, "html.parser")

    result = soup.select_one("body > div.l-contents.mt10 > main > div.pairbox > div:nth-child(2) > div > div.pairbox__rate > span.pairbox__rate__item")
    return "💰 " + result.get_text() + " yen/1euro"


def get_appartements_info():
    browser = setup()
    browser.get(os.environ["APARTMENTS_URL"])
    
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

