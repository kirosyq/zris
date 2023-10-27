'''
chains : arbitrum | optimism | bsc | polygon | base | avalanche | ethereum | scroll | zksync | linea | nova | zora
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
USE_PROXY = True # Enable/disable proxy usage in web3 requests

class ValueMintBridge:
    '''mint + bridge'''

    from_chain  = ['nova'] # Randomly selected from cheaper networks if empty
    to_chain    = ['polygon', 'optimism', 'bsc'] # Randomly selected from cheaper networks if empty
    max_price = 3 # USD

    amount = [1, 2] # Range of NFTs to mint and bridge from the 'from_chain' network


class ValueMint:
    '''mint'''

    chain = ['nova', 'zksync', 'zora']
    amount_mint = [2, 4] # Range of NFTs to mint

class ValueBridge:
    """
    Bridge
    Searches for NFTs in 'from_chain' and, upon finding any, bridges them to a network randomly selected from 'to_chain'.
    """

    from_chain = ['nova']  # List of networks to search for NFTs
    to_chain = ['optimism', 'scroll', 'arbitrum', 'bsc', 'avalanche', 'base', 'linea']  # List of potential destination networks selected randomly

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
