[![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=Zerius_AIO)](https://git.io/typing-svg)

zerius_aio is a script that enables comprehensive interaction with https://zerius.io/. For more detailed information about the project, visit: https://t.me/hodlmodeth/338 (rus)

## Modules:
1. **ultra** - Identifies the most affordable networks where your native token balance is >= $1, locates NFTs, and bridges them to the most cost-effective networks. If there are no NFTs in the wallet, it mints and then initiates bridging. The bridging frequency is adjustable. For instance, if you set it to bridge twice, it will execute as follows: mint nft (base), bridge base => arbitrum => zksync.
2. **mint + bridge** - Mints and bridges NFTs from a selected network to another.
3. **mint** - Mints NFTs in the selected network.
4. **bridge** - Bridges NFTs from one network to another selected network.
5. **checker** - Observes the quantity of NFTs in the wallets across various networks.

## Algorithm of the 'ultra' module:
1. Compiles a list of all networks where there is a native token (>= $1) for bridging.
2. Determines the top 3 most affordable bridges for each network from 'included_chains'.
3. Calculates the minting cost for each network.
4. Selects the top 3 most affordable networks for mint + bridge and decides which network to start with. However, if 'from_chain' contains a list of networks, it randomly selects one as the initial for minting and the first bridge.
5. If NFTs already exist in the first network, no minting occurs. If not, NFT is minted.
6. Minting happens only in the first network; subsequent actions only involve bridging.
7. Randomly chooses 1 out of the top 3 most affordable networks for each action.

## Setup

1. All configurations are handled within the `settings.py` file, with descriptions provided therein.
2. Rename `wallets_EXAMPLE.txt` to `wallets.txt` and `data_EXAMPLE.py` to `data.py`.
3. In `wallets.txt`, enter the private keys for the wallets, each on a new line.
4. Execute the `main.py` file to run the script.

## Dependency Installation

Install the necessary libraries using pip: `pip install -r requirements.txt`


# Readme на русском.

zerius_aio - это скрипт, который умеет делать все в https://zerius.io/. Почитать подробнее о проекте здесь : https://t.me/hodlmodeth/338

## Модули : 
1. Ultra - ищет самые дешевые сети, в которых у тебя баланс нативки >= 1$, ищет нфт и бриджит в другие самые дешевые сети. если нфт в кошельке нет, сминтит и затем начнет бриджить. сколько раз бриджить - настраиваемое число. например, если ты указал бриджить 2 раза, то он (это пример) сделает так : mint nft (base), bridge base => arbitrum => zksync.
2. Mint + Bridge - минт + бридж нфт из выбранной сети в другую выбранную сеть.
3. Mint - минт нфт в выбранной сети.
4. Bridge - бридж нфт из одной сети в другую выбранную сеть.
5. Checker - смотрит в каких сетях сколько нфт есть на кошельках.

## Алгоритм ultra модуля :
1. Формирование списка всех сетей, где есть нативный токен (>= 1$) для бриджа
2. Поиск топ 3 самых дешевых бриджа для каждой сети из included_chains
3. Расчет стоимости минта NFT для каждой сети.
4. Выбирает топ 3 самые дешевые сети для минт + бридж, выбирает с какой сети начать. но если в from_chain есть список сетей, тогда выбирает одну сеть (рандомно) как первую для минта и первого бриджа
5. Если NFT в начальной сети уже есть, минт делаться не будет. Если нет - NFT минтится
6. Минт NFT происходит только в начальной сети, дальше NFT будет только бриджиться
7. Выбирается всегда 1 из топ 3 самых дешевых сетей (рандомно)

## Настройка.

1. Вся настройка делается в файле `setting.py`, описание там же. 
2. Переименуй файлы `wallets_EXAMPLE.txt` => `wallets.txt`, `data_EXAMPLE.py` => `data.py`.
3. В `wallets.txt` записывай приватники от кошельков с новой строки.
4. Запускать нужно файл `main.py`.

### Starknet mint
Если хочешь использовать mint модуль для старкнета:
1. Запиши в `starknet_wallets.txt` приватники от кошельков argent/braavos с новой строки.
2. Запиши в `starknet_addresses.txt` адреса от кошельков в том же порядке, что и приватники.

Устанавливаем библиотеки : `pip install -r requirements.txt`

Creared by https://t.me/hodlmodeth & https://github.com/polypox 
Zerius : https://zerius.io/  
Links : https://t.me/links_hodlmodeth  
