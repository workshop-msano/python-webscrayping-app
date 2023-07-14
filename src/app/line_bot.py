from linebot import LineBotApi
from linebot.models import TextSendMessage
import os

def post(contents):
    channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
    group_id = os.environ['LINE_GROUP_ID']
    msg = contents

    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(group_id, TextSendMessage(text=msg))
