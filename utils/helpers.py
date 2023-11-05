from data import DATA, TG_TOKEN, TG_ID
from setting import MAX_GWEI

import time
from loguru import logger
from web3 import Web3
import random
import asyncio
from eth_account import Account
import telebot
import math
import asyncio, aiohttp
from tqdm import tqdm


list_send = []
def send_msg():

    try:
        str_send = '\n'.join(list_send)
        bot = telebot.TeleBot(TG_TOKEN)
        bot.send_message(TG_ID, str_send, parse_mode='html')  

    except Exception as error: 
        logger.error(error)

def round_to(num, digits=3):
    try:
        if num == 0: return 0
        scale = int(-math.floor(math.log10(abs(num - int(num))))) + digits - 1
        if scale < digits: scale = digits
        return round(num, scale)
    except: return num

def get_base_gas():
    try:
        
        web3 = Web3(Web3.HTTPProvider(DATA['ethereum']['rpc']))
        gas_price = web3.eth.gas_price
        gwei_gas_price = web3.from_wei(gas_price, 'gwei')
        return gwei_gas_price
    
    except Exception as error: 
        logger.error(error)
        return get_base_gas()

def wait_gas():

    logger.info(f'check gas')
    while True:

        current_gas = get_base_gas()

        if current_gas > MAX_GWEI:
            logger.info(f'current_gas : {current_gas} > {MAX_GWEI}')
            time.sleep(60)
        else: break

def is_private_key(key):
    try:
        return Account().from_key(key).address
    except:
        return False

async def async_sleeping(from_sleep, to_sleep):
    x = random.randint(from_sleep, to_sleep)
    for i in tqdm(range(x), desc='sleep ', bar_format='{desc}: {n_fmt}/{total_fmt}'):
        await asyncio.sleep(1)
    
def intToDecimal(qty, decimal):
    return int(qty * 10**decimal)

def decimalToInt(qty, decimal):
    return int(qty / 10**decimal)

async def fetch_price(session, symbol):
    url = f'https://min-api.cryptocompare.com/data/price?fsym={symbol}&tsyms=USDT'

    try:
        async with session.get(url, timeout=10) as resp:
            if resp.status == 200:
                resp_json = await resp.json(content_type=None)
                return float(resp_json.get('USDT', 0))
            else:
                await asyncio.sleep(1)
                return await fetch_price(session, symbol)
    except Exception as error:
        await asyncio.sleep(1)
        return await fetch_price(session, symbol)
    
def sleeping(from_sleep, to_sleep):
    x = random.randint(from_sleep, to_sleep)
    for i in tqdm(range(x), desc='sleep ', bar_format='{desc}: {n_fmt}/{total_fmt}'):
        time.sleep(1)
    
async def get_chain_prices():
    chains = {
        'avalanche': 'AVAX',
        'polygon': 'MATIC',
        'ethereum': 'ETH',
        'bsc': 'BNB',
        'arbitrum': 'ETH',
        'optimism': 'ETH',
        'fantom': 'FTM',
        'zksync': 'ETH',
        'nova': 'ETH',
        'gnosis': 'xDAI',
        'celo': 'CELO',
        'polygon_zkevm': 'ETH',
        'core': 'COREDAO',
        'harmony': 'ONE',
        'moonbeam': 'GLMR',
        'moonriver': 'MOVR',
        'linea': 'ETH',
        'base': 'ETH',
        'scroll': 'ETH',
        'zora': 'ETH'
    }

    prices = {chain: 0 for chain in chains.keys()}

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_price(session, symbol) for symbol in chains.values()]
        fetched_prices = await asyncio.gather(*tasks)

        for chain, price in zip(chains.keys(), fetched_prices):
            prices[chain] = price
            if price == 0:
                logger.error(f'Failed to fetch price for {chain}. Setting price to 0.')

    return prices