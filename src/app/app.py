from app import scraper, line_bot, slack_bot
from dotenv import load_dotenv

load_dotenv()

def handler(event=None, context=None):
    currency_data = ""
    while currency_data == "":
        currency_data = scraper.get_currency_trend()
    print("currency_data: ", currency_data)
    line_bot.post(currency_data)

    apt_data = ""
    while apt_data == "":
        apt_data = scraper.get_appartements_info()
        print("apt_data: ", len(apt_data))
    if len(apt_data) > 4900 : #もし5000文字以上の場合、LINEが一度に送信できる5000文字ずつ分割する
        split_text = [apt_data[x:x+4900] for x in range(0, len(apt_data), 4900)]
        num = 0
        for x in split_text:
                print(f"result {num}: {len(x)}")
                line_bot.post(x)
                num += 1
    else: 
        line_bot.post(apt_data)

    slack_bot.post(apt_data)

if __name__ == "__main__":
    handler()
