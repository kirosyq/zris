'''
chains : arbitrum | optimism | bsc | polygon | base | avalanche | ethereum | scroll | zksync
'''

RETRY               = 0     # Количество попыток при ошибках/фейлах
WALLETS_IN_BATCH    = 1     # Сколько кошельков запускаем в одном потоке (одновременно)
CHECK_GWEI          = True  # Включить/выключить проверку base Gwei
MAX_GWEI            = 40    # Максимальный Gwei (см. https://etherscan.io/gastracker)
TG_BOT_SEND         = True  # Включить/выключить отправку результатов в Telegram-бота
IS_SLEEP            = True  # Включить/выключить задержку между кошельками
DELAY_SLEEP         = [3, 5] # Диапазон задержки между кошельками (секунды)
RANDOMIZER          = True  # Включить/выключить случайное перемешивание кошельков
MAX_WAITING_NFT     = 120   # Сколько максимум по времени (sec.) ждем нфт после бриджа в destination chain

class ValueMintBridge:
    '''mint + bridge'''

    from_chain  = ['bsc', 'arbitrum'] # рандомно выбираем из дешевых сетей, если пусто
    to_chain    = ['scroll', 'optimism'] # рандомно выбираем из дешевых сетей, если пусто
    max_price = 3 # $

    amount = [1, 2] # от скольки до скольки нфт минтим + бриджим из сети from_chain

class ValueMint:
    '''mint'''

    chain = ['zksync', 'arbitrum', 'base']
    amount_mint = [1, 4] # от скольки до скольки нфт минтим

class ValueBridge:
    '''
    bridge
    ищет nft в from_chain и с первой сети где найдет, бриджит на сеть из to_chain которая выберется рандомно
    '''

    from_chain  = ['arbitrum', 'optimism']
    to_chain    = ['bsc', 'base', 'zksync']

    amount = 1 # сколько нфт бриджим из сети from_chain
    bridge_all = True # True / False. True если хочешь сбриджить все нфт которые у тебя есть в сети from_chain если их больше amount

class ValueUltra:
    '''
    1. составляет список всех сетей, где есть нативный токен (>= 1$) для бриджа
    2. ищет топ 3 самых дешевых бриджа для каждой сети из included_chains
    3. вычисляет стоимость минта для каждой сети
    4. выбирает топ 3 самые дешевые сети для минт + бридж, выбирает с какой сети начать. но если в from_chain есть список сетей, тогда выбирает одну сеть (рандомно) как первую для минта и первого бриджа
    5. если нфт в первой сети уже есть, минта не будет. если нет - нфт минтится
    6. минт происходит только в первой сети, дальше нфт будет только бриджиться
    7. выбирается всегда 1 из топ 3 самых дешевых сетей (рандомно)
    '''

    max_bridge_price = 2 # $ если бридж с этой сети стоит дороже, эта сеть не выберется для бриджа
    bridges_count = [1, 4]
    from_chain = [] # можно оставить пустым, тогда скрипт сам выберет самую дешевую сеть из списка included_chains
    included_chains = ['optimism', 'scroll', 'arbitrum', 'bsc', 'avalanche', 'base'] # >= 2 сетей
