# Phone Marketplace Telegram Bot

A Telegram bot that allows users to post and search for phones for sale.

## Features

- Post phones for sale with:
  - Phone name
  - Category (iPhone, Samsung, Xiaomi, Huawei, Other)
  - Description
  - Price
  - Photo
  - Seller's username
- Search phones by category
- In-memory storage of listings

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Get a Telegram Bot Token:
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Create a new bot using the `/newbot` command
   - Copy the token provided by BotFather

3. Update the bot token:
   - Open `phone_marketplace_bot.py`
   - Replace `'YOUR_BOT_TOKEN'` with your actual bot token

4. Run the bot:
```bash
python phone_marketplace_bot.py
```

## Usage

1. Start the bot by sending `/start`
2. Choose between:
   - "Post a Phone" - to create a new listing
   - "Search Phones" - to browse existing listings

### Posting a Phone
1. Enter the phone name
2. Select the category
3. Provide a description
4. Enter the price
5. Send a photo of the phone

### Searching Phones
1. Select a category
2. Browse through the available listings
3. Contact sellers using their Telegram username

## Note
This bot stores listings in memory, so all data will be lost when the bot is restarted. For a production environment, you should implement a database solution. 