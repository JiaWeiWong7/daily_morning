from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_countB():
  delta = today - datetime.strptime("2021-11-5", "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_birthdayB():
  next = datetime.strptime(str(date.today().year) + "-" + "10-03", "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)
client2 = WeChatClient("wx43670927a37a0863", "4fcef27194be995c9cf7de76531f732a")

wm = WeChatMessage(client)
wm2 = WeChatMessage(client2)

wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
data2 = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_countB()},"birthday_left":{"value":get_birthdayB()},"words":{"value":get_words(), "color":get_random_color()}}

res = wm.send_template(user_id, template_id, data)
res2 = wm2.send_template("okf1F6Mx5dcSMTDgGoYtMl81UE9Y", "Zg_p9Q6_ZsAWaThtMh_OLP-GmQ9iiGeNlYuLPSMgqBg", data2)
print(res)
print(res2)
