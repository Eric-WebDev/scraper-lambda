import boto3
import requests
import json
from datetime import datetime
import shortuuid
from bs4 import BeautifulSoup

dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    scraper_put()

def scraper_put():
    bitcoin = requests.get(
        'https://coinmarketcap.com/currencies/bitcoin/markets/')
    etherum = requests.get('https://coinmarketcap.com/currencies/ethereum/')
    soup1 = BeautifulSoup(bitcoin.content, 'html.parser')
    soup2 = BeautifulSoup(etherum.content, 'html.parser')
    price_bitcoin = soup1.find('div', attrs={'priceValue___11gHJ'}).get_text()
    price_etherum = soup2.find('div', attrs={'priceValue___11gHJ'}).get_text()
    table = dynamodb.Table('Currencies')
    date_time = datetime.now()
    date_time_string = date_time.strftime("%m/%d/%Y, %H:%M:%S")

    response = table.put_item(
        Item={
            'id': shortuuid.uuid(),
            'bitcoin': price_bitcoin,
            'etherum': price_etherum,
            'dateTime': date_time_string
        }
    )
    return response
