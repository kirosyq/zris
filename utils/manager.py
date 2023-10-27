from data import DATA
from setting import USE_PROXY
from config import max_time_check_tx_status, PROXIES
import time
from loguru import logger
from web3 import Web3, AsyncHTTPProvider
from web3.eth import AsyncEth
import random
import asyncio

class Web3Manager:
    def __init__(self, key, chain):
        self.key = key
        self.chain = chain
        self.web3 = self.get_web3()
        self.address = self.web3.eth.account.from_key(self.key).address
        self.chain_id = DATA[self.chain]['chain_id']
    
    def get_web3(self):
        rpc = DATA[self.chain]['rpc']
        web3 = Web3(AsyncHTTPProvider(rpc), modules={"eth": (AsyncEth)}, middlewares=[])

        if USE_PROXY:
            try:
                proxy = random.choice(PROXIES)
                web3 = Web3(AsyncHTTPProvider(rpc, request_kwargs={"proxy": proxy}), modules={"eth": (AsyncEth)}, middlewares=[])
            except Exception as error:
                logger.error(f'{error}. Use web3 without proxy')

        return web3
    
    async def add_gas_limit(self, contract_txn):

        value = contract_txn['value']
        contract_txn['value'] = 0
        pluser = [1.02, 1.05]
        gasLimit = await self.web3.eth.estimate_gas(contract_txn)
        contract_txn['gas'] = int(gasLimit * random.uniform(pluser[0], pluser[1]))

        contract_txn['value'] = value
        return contract_txn
    
    async def sign_tx(self, contract_txn):

        signed_tx = self.web3.eth.account.sign_transaction(contract_txn, self.key)
        raw_tx_hash = await self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_hash = self.web3.to_hex(raw_tx_hash)
        
        return tx_hash
    
    async def get_status_tx(self, tx_hash):

        logger.info(f'{self.chain} : checking tx_status : {tx_hash}')
        start_time_stamp = int(time.time())

        while True:
            try:
                receipt = await self.web3.eth.get_transaction_receipt(tx_hash)
                status = receipt["status"]
                if status in [0, 1]:
                    return status

            except Exception as error:
                time_stamp = int(time.time())
                if time_stamp-start_time_stamp > max_time_check_tx_status:
                    logger.info(f"didn't get tx_status in {max_time_check_tx_status} sec, thinks tx is failed")
                    return 0
                await asyncio.sleep(1)

    async def send_tx(self, contract_txn):

        tx_hash = await self.sign_tx(contract_txn)
        status  = await self.get_status_tx(tx_hash)
        tx_link = f'{DATA[self.chain]["scan"]}/{tx_hash}'

        return status, tx_link

    async def add_gas_limit_layerzero(self, contract_txn):

        pluser = [1.05, 1.07]
        gasLimit = await self.web3.eth.estimate_gas(contract_txn)
        contract_txn['gas'] = int(gasLimit * random.uniform(pluser[0], pluser[1]))
        return contract_txn

    async def add_gas_price(self, contract_txn):

        if self.chain == 'bsc':
            contract_txn['gasPrice'] = 1000000000 # Intentionally setting 1 Gwei to make the transaction cheaper
        else:
            gas_price = await self.web3.eth.gas_price
            contract_txn['gasPrice'] = int(gas_price * random.uniform(1.01, 1.02))
        return contract_txn
