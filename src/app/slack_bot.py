import os, requests

def post(contents):
    url = "https://slack.com/api/chat.postMessage"
    token = os.environ["SLACK_BOT_USER_OAUTH_TOKEN"]

    header={
        "Authorization": "Bearer {}".format(token)
        }
    data  = {
        "channel" : os.environ["SLACK_CHANNEL"],
        "text" : contents
        }

    slack_res = requests.post(url, headers=header, json=data)

    resonse_json = slack_res.json()
    print("response from Slack: ",resonse_json)
