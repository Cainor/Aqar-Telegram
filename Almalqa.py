#!/usr/bin/env python
# coding: utf-8

#Must configure your own telegram bot.

import telegram_send
from sys import exit
import requests
import json
from time import sleep
import datetime


timeToSleep = 60*2


#F12 in your browser, and navigate to Network tab.
#Then browse district you want to look up. Look for "graphql" request, take the data from there.
category = 1
city_id = 21 #Riyadh
direction_id = 4 # 1-South 3-East 4-North 6-West 7-Middle (Maybe)
district_id = 570 #570 Almalqa
rent_period = 3 #Yearly

burp0_cookies = {"_ga": "GA1.2.827713667.1659630037", "AWSALBTG": "8pK4acwkfex/oD2IQ02w6e+PZzplC/1lVz9q6Pbjy8Fx60AL2stUaRP4EWH38mqdHHxF24k9tjIOLydD0s0AfiyluTDiXgOKOtn6NPbvcYSzxOyXWKo5C0OXgtx+MviFlvTUV2nl6yN29ZS5xGnxxCv+OAxbvSyBCuH2d6W9DZMtabP39lA=", "AWSALBTGCORS": "8pK4acwkfex/oD2IQ02w6e+PZzplC/1lVz9q6Pbjy8Fx60AL2stUaRP4EWH38mqdHHxF24k9tjIOLydD0s0AfiyluTDiXgOKOtn6NPbvcYSzxOyXWKo5C0OXgtx+MviFlvTUV2nl6yN29ZS5xGnxxCv+OAxbvSyBCuH2d6W9DZMtabP39lA="}
burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"103\", \".Not/A)Brand\";v=\"99\"", "Req-App": "web", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36", "Viewport-Width": "1704", "Content-Type": "application/json", "Accept": "*/*", "App-Version": "0.16.15", "Req-Device-Token": "d7801545-e168-449f-847c-f93c80554a69", "Dpr": "1", "Sec-Ch-Ua-Platform": "\"Windows\"", "Origin": "https://sa.aqar.fm", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://sa.aqar.fm/%D8%B4%D9%82%D9%82-%D9%84%D9%84%D8%A5%D9%8A%D8%AC%D8%A7%D8%B1/%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6/%D8%B4%D9%85%D8%A7%D9%84-%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6/%D8%AD%D9%8A-%D8%A7%D9%84%D9%85%D9%84%D9%82%D8%A7/2?rent_type=3", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}
burp0_url = "https://sa.aqar.fm:443/graphql"    
burp0_json={"operationName": "findListings", "query": "query findListings($size: Int, $from: Int, $sort: SortInput, $where: WhereInput, $polygon: [LocationInput!]) {\n  Web {\n    find(size: $size, from: $from, sort: $sort, where: $where, polygon: $polygon) {\n      ...WebResults\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment WebResults on WebResults {\n  listings {\n    user_id\n    id\n    uri\n    title\n    price\n    content\n    imgs\n    refresh\n    category\n    beds\n    livings\n    wc\n    area\n    type\n    street_width\n    age\n    last_update\n    street_direction\n    ketchen\n    ac\n    furnished\n    location {\n      lat\n      lng\n      __typename\n    }\n    path\n    user {\n      review\n      img\n      name\n      phone\n      iam_verified\n      rega_id\n      __typename\n    }\n    native {\n      logo\n      title\n      image\n      description\n      external_url\n      __typename\n    }\n    rent_period\n    city\n    district\n    width\n    length\n    advertiser_type\n    create_time\n    __typename\n  }\n  total\n  __typename\n}\n", "variables": {"from": 0, "size": 100, "sort": {"create_time": "desc"}, "where": {"category": {"eq": category}, "city_id": {"eq": city_id}, "direction_id": {"eq": direction_id}, "district_id": {"eq": district_id}, "rent_period": {"eq": rent_period}}}}


addedTime = 0
def CheckAqar():
    change = False
    result = ""
    global addedTime
    print("Checking ...")
    
    #Find current posts
    if(addedTime == 0):
        print("Getting the current listing")
        res = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, json=burp0_json).json()
        res = res['data']['Web']['find']['listings']
        res = sorted(res, key=lambda x : x['create_time'], reverse=True)
        addedTime = res[0]["create_time"]
        print("Last post was on: ",  datetime.datetime.fromtimestamp(addedTime))
        print("https://sa.aqar.fm/"+res[0]["path"])
        return False,"None"

    #Check if new posts are found
    else:
        res = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, json=burp0_json).json()
        res = res['data']['Web']['find']['listings']
        res = sorted(res, key=lambda x : x['create_time'], reverse=True)
        if(res[0]["create_time"] > addedTime):
            print("newly added")
            addedTime = res[0]["create_time"]
            change = True
            result = "Almalqa -- https://sa.aqar.fm/"+res[0]["path"]
        return change,result


def main():
    try:
        while(True):
            #Check Aqar
            change, result = CheckAqar()
            if(change):
                telegram_send.send(messages=["New rentals in: \r\n "+result],conf="telegram_conf.txt")
                
            sleep(timeToSleep)
    except:
        telegram_send.send(messages=["Something went wrong :\\"],conf="telegram_conf.txt")
        exit()

# telegram_conf.txt is a file that contains your token and your chat_id. The template looks like this:
# [telegram]
# token = TOKEN
# chat_id = ID

main()

