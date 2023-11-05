from pathlib import Path
import asyncio
from utils.helpers import get_chain_prices
from utils.files import read_txt, load_json

max_time_check_tx_status = 100
WALLETS = read_txt("wallets.txt")
PROXIES = read_txt("proxies.txt")

contracts = {
    'ethereum': '0x178608fFe2Cca5d36f3Fc6e69426c4D3A5A74A41', 
    'optimism': '0x178608fFe2Cca5d36f3Fc6e69426c4D3A5A74A41', 
    'bsc': '0x250c34D06857b9C0A036d44F86d2c1Abe514B3Da', 
    'polygon': '0x178608fFe2Cca5d36f3Fc6e69426c4D3A5A74A41', 
    'arbitrum': '0x250c34D06857b9C0A036d44F86d2c1Abe514B3Da', 
    'avalanche': '0x178608fFe2Cca5d36f3Fc6e69426c4D3A5A74A41', 
    'base': '0x178608fFe2Cca5d36f3Fc6e69426c4D3A5A74A41',
    'zora': '0x178608fFe2Cca5d36f3Fc6e69426c4D3A5A74A41',
    'scroll': '0xEB22C3e221080eAD305CAE5f37F0753970d973Cd',
    'zksync': '0x7dA50bD0fb3C2E868069d9271A2aeb7eD943c2D6',
    'linea': '0x5188368a92B49F30f4Cf9bEF64635bCf8459c7A7',
    'nova': '0x5188368a92B49F30f4Cf9bEF64635bCf8459c7A7',
    'metis': '0x5188368a92B49F30f4Cf9bEF64635bCf8459c7A7',
    'moonbeam': '0x4c5AeDA35d8F0F7b67d6EB547eAB1df75aA23Eaf',
    'polygon_zkevm': '0x4c5AeDA35d8F0F7b67d6EB547eAB1df75aA23Eaf',
    'core': '0x5188368a92B49F30f4Cf9bEF64635bCf8459c7A7',
    'celo': '0x4c5AeDA35d8F0F7b67d6EB547eAB1df75aA23Eaf',
    'harmony': '0x5188368a92B49F30f4Cf9bEF64635bCf8459c7A7',
    'canto': '0x5188368a92B49F30f4Cf9bEF64635bCf8459c7A7',
    'fantom': '0x5188368a92B49F30f4Cf9bEF64635bCf8459c7A7',
    'gnosis': '0x5188368a92B49F30f4Cf9bEF64635bCf8459c7A7',
}


ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'

LAYERZERO_CHAINS_ID = {
    'avalanche' : 106,
    'polygon'   : 109,
    'ethereum'  : 101,
    'bsc'       : 102,
    'arbitrum'  : 110,
    'optimism'  : 111,
    'fantom'    : 112,
    'aptos'     : 108,
    'harmony'   : 116,
    'celo'      : 125,
    'moonbeam'  : 126,
    'fuse'      : 138,
    'gnosis'    : 145,
    'klaytn'    : 150,
    'metis'     : 151,
    'core'      : 153,
    'polygon_zkevm': 158,
    'canto'     : 159,
    'moonriver' : 167,
    'tenet'     : 173,
    'nova'      : 175,
    'kava'      : 177,
    'meter'     : 176,
    'base'      : 184,
    'zora'      : 195,
    'scroll'    : 214,
    'zksync'    : 165,
    'linea'     : 183,
}

EXCLUDED_LZ_PAIRS = [
    (195, 102), # zora => bsc
    (195, 106), # zora => avalanche
    (214, 195), # scroll => zora
    (214, 184), # scroll => base
    (165, 214), # zksync => scroll
    (165, 195), # zksync => zora
    (183, 195), # linea => zora
    (183, 214), # linea => scroll
    (175, 158), # nova => polygon_zkevm
    (175, 195), # nova => zora
    (175, 214), # nova => scroll
    (175, 183), # nova => linea
    (175, 153), # nova => core
    (175,  125), # nova => celo
    (175, 116), # nova => harmony
    (175, 145), # nova => gnosis
    (151, 195), 
    (151, 214),
    (151, 165), 
    (151, 126), 
    (151, 153), 
    (151, 125), 
    (151, 116),
    (126, 195), 
    (126, 214), 
    (126, 165), 
    (126, 183), 
    (126, 151), 
    (126, 158), 
    (126, 153), 
    (126, 125), 
    (126, 159),
    (158, 195), 
    (158, 214), 
    (158, 175), 
    (158, 126), 
    (158, 153), 
    (158, 116), 
    (158, 159),
    (153, 175), 
    (153, 158), 
    (153, 184), 
    (153, 195), 
    (153, 214), 
    (153, 165), 
    (153, 183), 
    (153, 151), 
    (153, 125), 
    (153, 116), 
    (153, 159), 
    (153, 112), 
    (153, 145),
    (125, 184), 
    (125, 195), 
    (125, 214),
    (125, 165), 
    (125, 183), 
    (125, 175), 
    (125, 151),
    (125, 126), 
    (125, 153), 
    (125, 116), 
    (125, 159),
    (116, 184), 
    (116, 195), 
    (116, 214), 
    (116, 165), 
    (116, 183), 
    (116, 175), 
    (116, 151), 
    (116, 158), 
    (116, 153), 
    (116, 125), 
    (116, 159), 
    (116, 145),
    (159, 184), 
    (159, 195), 
    (159, 214), 
    (159, 183), 
    (159, 126), 
    (159, 158), 
    (159, 153), 
    (159, 125), 
    (159, 116), 
    (159, 145),
    (112, 195), 
    (112, 214), 
    (112, 153),
]
ZERIUS_SEND_GAS_LIMIT = {
    101: 300000,
    110: 650000,
    111: 300000,
    109: 300000,
    102: 300000,
    106: 300000,
    184: 300000,
    195: 300000,
    214: 300000,
    165: 1800000,
    175: 300000, # nova
    183: 300000, # linea
}
ZERIUS_MINT_GAS_LIMIT = {
    101: 170000,
    110: 350000,
    111: 170000,
    109: 170000,
    102: 170000,
    106: 170000,
    184: 170000,
    195: 170000,
    214: 170000,
    165: 1000000,
    175: 170000, # nova
    183: 170000, # linea
}
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies=usd"
LZ_CHAIN_TO_TOKEN = {
    101: 'ETH',
    110: 'ETH',
    111: 'ETH',
    109: 'MATIC',
    102: 'BNB',
    106: 'AVAX',
    184: 'ETH',
    195: 'ETH',
    214: 'ETH',
    165: 'ETH',
    175: 'ETH',   # nova
    183: 'ETH',   # linea
    112: 'FTM',   # fantom
    158: 'ETH',   # polygon zkEVM
    153: 'CORE',  # Core
    125: 'CELO',  # Celo
    116: 'ONE',   # Harmony
    159: 'CANTO', # Canto
}

REFUEL_CONTRACTS = {
    'optimism'      : '0x2076BDd52Af431ba0E5411b3dd9B5eeDa31BB9Eb',
    'bsc'           : '0x5B209E7c81DEaad0ffb8b76b696dBb4633A318CD',
    'arbitrum'      : '0x412aea168aDd34361aFEf6a2e3FC01928Fba1248',
    'polygon'       : '0x2ef766b59e4603250265EcC468cF38a6a00b84b3',
    'polygon_zkevm' : '0xBAf5C493a4c364cBD2CA83C355E75F0ff7042945',
    # 'zksync'        : '' # temp unavailable,
    'avalanche'     : '0x5B209E7c81DEaad0ffb8b76b696dBb4633A318CD',
    'gnosis'        : '0x1fe2c567169d39CCc5299727FfAC96362b2Ab90E',
    'fantom'        : '0xBFd3539e4e0b1B29e8b08d17f30F1291C837a18E',
    'nova'          : '0x3Fc5913D35105f338cEfcB3a7a0768c48E2Ade8E',
    'harmony'       : '0x5B209E7c81DEaad0ffb8b76b696dBb4633A318CD', # unavailable : need to convert it to a one-address
    'core'          : '0xB47D82aA70f839dC27a34573f135eD6dE6CED9A5',
    'celo'          : '0xFF21d5a3a8e3E8BA2576e967888Deea583ff02f8',
    'moonbeam'      : '0xb0bea3bB2d6EDDD2014952ABd744660bAeF9747d',
    'base'          : '0x9415AD63EdF2e0de7D8B9D8FeE4b939dd1e52F2C',
    'scroll'        : '0xB074f8D92b930D3415DA6bA80F6D38f69ee4B9cf',
    'zora'          : '0x1fe2c567169d39CCc5299727FfAC96362b2Ab90E',
    'linea'         : '0x5B209E7c81DEaad0ffb8b76b696dBb4633A318CD',
    'metis'         : '0x1b07F1f4F860e72c9367e718a30e38130114AD22',
}

REFUEL_MAX_CAPS = {
    'avalanche' : 18.47,
    'polygon'   : 681,
    'ethereum'  : 0.24,
    'bsc'       : 1.32,
    'arbitrum'  : 0.24,
    'optimism'  : 0.24,
    'fantom'    : 1304,
    'harmony'   : 0.05,
    'celo'      : 10,
    'moonbeam'  : 10,
    'gnosis'    : 0.05,
    'metis'     : 0.05,
    'core'      : 0.25,
    'polygon_zkevm': 0.05,
    'canto'     : 0.05,
    'nova'      : 0.05,
    'base'      : 0.05,
    'zora'      : 0.05,
    'scroll'    : 0.05,
    'zksync'    : 0.05,
    'linea'     : 0.05,
}

STR_DONE = '✅ '
STR_CANCEL = '❌ '

PRICES_NATIVE = asyncio.run(get_chain_prices())

ABI = load_json("utils/abi/abi.json")
REFUEL_ABI = load_json("utils/abi/refuel.json")
ERC20_ABI = load_json("utils/abi/erc20.json")