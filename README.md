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
