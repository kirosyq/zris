import asyncio
from utils.helpers import get_chain_prices
from utils.files import read_txt, load_json
    
max_time_check_tx_status = 100
WALLETS = read_txt("data/wallets.txt")
PROXIES = read_txt("data/proxies.txt")
STARKNET_KEYS = read_txt("data/starknet_keys.txt")
STARKNET_ADDRESSES = read_txt("data/starknet_addresses.txt")

STARKNET_MAX_MINT_GAS = 500000000000000
STARKNET_MAX_APPROVE_GAS = 300000000000000
STARKNET_RPC = "https://g.w.lavanet.xyz:443/gateway/strk/rpc-http/f7ee0000000000000000000000000000"
STARKNET_SCANNER = "https://voyager.online/tx"
STARKNET_ETH_ADDRESS = "0x049D36570D4e46f48e99674bd3fcc84644DdD6b96F7C741B1562B82f9e004dC7"
STARKNET_ADDRESS = "0x043ba5e69eec55ce374e1ce446d16ee4223c1ba48c808d2dcd4e606f94ec9e15"

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
    'mantle': '0x5188368a92B49F30f4Cf9bEF64635bCf8459c7A7',
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
    'mantle'    : 181,
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
    (175, 125), # nova => celo
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
    (126, 145),
    (101, 153),
    (101, 151),
    (101, 158),
    (101, 175),
    (145, 165),
    (145, 183),
    (145, 214),
    (151, 106),
    (151, 111),
    (151, 109), 
    (151, 110),
    (151, 112),
    (151, 102),
    (151, 158),
    (151, 159),
    (151, 145),
    (151, 175),
    (151, 184),
    (151, 183),
    (101, 125),
    (101, 126),
    (101, 214),
    (101, 165),
    (101, 184),
    (101, 159),
    (101, 183),
    (165, 158),
    (165, 112),
    (165, 159),
    (165, 175),
    (165, 183),
    (101, 106),
    (101, 109),
    (101, 102),
    (101, 111),
    (101, 110),
    (101, 112),
    (101, 145),
    (116, 101),
    (116, 125),
    (116, 126),
    (116, 151),
    (116, 153),
    (116, 158),
    (116, 159),
    (116, 175),
    (116, 184),
    (116, 214),
    (116, 165),
    (116, 183),
    (181, 101),
    (181, 195),
    (181, 214),
    (181, 165),
    (181, 175),
    (181, 126),
    (181, 116),
    (181, 181),
    (181, 159),
    (181, 125),
    (181, 153),
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
    112: 300000,
    158: 300000,
    153: 300000,
    125: 300000,
    116: 300000,
    159: 300000,
    126: 300000,
    151: 300000,
    145: 300000,
    181: 300000,
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
    112: 170000,
    158: 170000,
    153: 170000,
    125: 170000,
    116: 170000,
    159: 170000,
    126: 170000,
    151: 170000,
    145: 170000,
    181: 170000,
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
    126: 'GLMR', # Moonbeam
    151: 'METIS', # Metis
    145: 'XDAI', # Gnosis
    181: 'MNT', # Mantle
}

REFUEL_CONTRACTS = {
    'optimism'      : '0x2076BDd52Af431ba0E5411b3dd9B5eeDa31BB9Eb',
    'bsc'           : '0x5B209E7c81DEaad0ffb8b76b696dBb4633A318CD',
    'arbitrum'      : '0x412aea168aDd34361aFEf6a2e3FC01928Fba1248',
    'polygon'       : '0x2ef766b59e4603250265EcC468cF38a6a00b84b3',
    'polygon_zkevm' : '0xBAf5C493a4c364cBD2CA83C355E75F0ff7042945',
    'zksync'        : '0xec8afef7afe586eb523c228b6baf3171b1f6dd95',
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
    'mantle'        : '0x4F1C698e5cA32b28030E9d9F17C164F27aB5D866',
}

STR_DONE = '✅ '
STR_CANCEL = '❌ '

PRICES_NATIVE = asyncio.run(get_chain_prices())

ABI = load_json("utils/abi/abi.json")
REFUEL_ABI = load_json("utils/abi/refuel.json")
ERC20_ABI = load_json("utils/abi/erc20.json")
STARKNET_ETH_ABI = load_json("utils/abi/starknet_eth_abi.json")