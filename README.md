# Aqar-Telegram
Alert of new posts in Aqar application through telegram.

## Telegram Bot
You can generate your own Telegram Bot by contacting "@BotFather". BotFather used to create new bot accounts and manage your existing bots.
Once you create it, you will be presented by a token to be used to trigger the notification. You can use it inside the "telegram_conf.txt" file.

Then you need to get your own ID to point your bot to contact you. You can retreive such information by contacting "@raw_data_bot". It will provide you with your ID.

Your "telegram_conf.txt" should look like this:
```
[telegram]
token = YOUR TOKEN HERE
chat_id = YOUR ID HERE
```

## Aqar settings
Settings are in the beginning of the "Almalqa.py" file:
```
category = 1
city_id = 21 #Riyadh
direction_id = 4 # 1-South 3-East 4-North 6-West 7-Middle (Maybe)
district_id = 570 #570 Almalqa
rent_period = 3 #Yearly
```

You can get such information by monitoring your traffic while browsing Aqar website. Specificly, the "graphql" endpoint.
