'''
chains : arbitrum | optimism | bsc | polygon | base | avalanche | ethereum | scroll | zksync | linea | nova | zora | polygon_zkevm | fantom | core | celo | harmony | canto
'''

RETRY = 0 # Number of attempts when errors/fails occur
WALLETS_IN_BATCH = 1 # How many wallets are launched in one thread (simultaneously)
CHECK_GWEI = True # Enable/disable checking of base Gwei
MAX_GWEI = 25 # Maximum Gwei (see https://etherscan.io/gastracker)
TG_BOT_SEND = True # Enable/disable sending results to the Telegram bot
IS_SLEEP = True # Enable/disable delay between wallets
DELAY_SLEEP = [50, 100] # Range of delay between wallets (seconds)
RANDOMIZER = True # Enable/disable random shuffling of wallets
MAX_WAITING_NFT = 120 # Maximum wait time (sec.) for NFTs after bridging to the destination chain
USE_PROXY = False # Enable/disable proxy usage in web3 requests

MAX_GAS_CHARGE = {
    'avalanche'     : 1,
    'polygon'       : 0.5,
    'ethereum'      : 3,
    'bsc'           : 0.3,
    'arbitrum'      : 1,
    'optimism'      : 1.5,
    'fantom'        : 0.5,
    'zksync'        : 1,
    'nova'          : 0.1,
    'gnosis'        : 0.1,
    'celo'          : 0.1,
    'polygon_zkevm' : 0.5,
    'core'          : 0.1,
    'harmony'       : 0.1,
    'base'          : 0.5,
    'scroll'        : 0.5,
    'zora'          : 0.5,
    'moonbeam'      : 0.5,
    'moonriver'     : 0.5,
    'canto'         : 0.5,
    'metis'         : 0.5,
}

class ValueMintBridge:
    '''mint + bridge'''

    from_chain  = ['nova'] # Randomly selected from cheaper networks if empty
    to_chain    = ['polygon', 'optimism', 'bsc'] # Randomly selected from cheaper networks if empty
    max_price = 3 # USD

    refuel_amount_from = 0 # Obtain from a certain amount of native token of the to_chain network
    refuel_amount_to   = 0 # Obtain up to a certain amount of native token of the to_chain network

    amount = [1, 2] # Range of NFTs to mint and bridge from the 'from_chain' network

class ValueMint:
    '''mint'''

    chain = ['harmony', 'celo', 'core']
    amount_mint = [2, 4] # Range of NFTs to mint

class ValueBridge:
    """
    Bridge
    Searches for NFTs in 'from_chain' and, upon finding any, bridges them to a network randomly selected from 'to_chain'.
    """

    from_chain = ['nova']  # List of networks to search for NFTs
    to_chain = ['optimism', 'scroll', 'arbitrum', 'bsc', 'avalanche', 'base', 'linea']  # List of potential destination networks selected randomly

    refuel_amount_from = 0 # Obtain from a certain amount of native token of the to_chain network
    refuel_amount_to   = 0 # Obtain up to a certain amount of native token of the to_chain network

    amount = 1  # The number of NFTs to bridge from the 'from_chain' network
    bridge_all = True  # True/False. If True, all available NFTs in the 'from_chain' network will be bridged if they exceed 'amount'.

class ValueUltra:
    """
    1. Compiles a list of all networks where there is a native token (>= $1) for bridging.
    2. Identifies the top 3 cheapest bridges for each network in 'included_chains'.
    3. Calculates the minting cost for each network.
    4. Selects the top 3 cheapest networks for mint + bridge and decides which network to start with. However, if 'from_chain' contains a list of networks, then one network is randomly selected as the first for minting and the initial bridge.
    5. If NFTs are already present in the first network, no minting will occur. If not, an NFT is minted.
    6. Minting occurs only in the first network; subsequently, the NFT will only be bridged.
    7. Always selects 1 out of the top 3 cheapest networks (randomly).
    """

    max_bridge_price = 1.5  # $ If the bridge from this network is more expensive, it will not be selected for bridging.
    bridges_count = [1, 3]  # The range for the number of bridges.
    from_chain = ['nova']  # Can be left empty, then the script will choose the cheapest network from 'included_chains'.
    included_chains = ['optimism', 'scroll', 'arbitrum', 'bsc', 'avalanche', 'base', 'linea']  # Must include >= 2 networks.

    refuel_amount_from = 0 # Obtain from a certain amount of native token of the to_chain network
    refuel_amount_to   = 0 # Obtain up to a certain amount of native token of the to_chain network


class ValueRefuel:

    '''
    Gas refuel via https://zerius.io/

    from_chains : optimism | bsc | polygon | arbitrum | avalanche | fantom | linea | celo | zksync (temp disabled) | polygon_zkevm | nova | canto | zora | scroll | harmony | gnosis | core | base | mantle
    to_chains   : avalanche | bsc | arbitrum | optimism | fantom | harmony | celo | moonbeam | gnosis | metis | core | polygon_zkevm | canto | zksync | nova | zora | base | scroll
    '''

    from_chain = ['linea'] # Networks from which you want to perform refuel (>= 1 network)
    to_chain   = ['base', 'avalanche', 'bsc', 'arbitrum'] # Networks to which you want to perform refuel (>= 1 network)

    amount_from         = 0.001 # Obtain from a certain amount of native token of the to_chain network
    amount_to           = 0.002 # Obtain up to a certain amount of native token of the to_chain network

    swap_all_balance    = False # True / False. If True, then refuel the entire balance
    min_amount_swap     = 0 # If the balance is less than this amount, no refuel will be made
    keep_value_from     = 0 # How many coins to keep on the wallet (only works when: swap_all_balance = True)
    keep_value_to       = 0 # Up to how many coins to keep on the wallet (only works when: swap_all_balance = True)

    get_layerzero_fee   = False # True if you want to check the gas. False if you want to perform refuel