from utils.modules import main
from utils.titles import TITLE, TITLE_COLOR
from termcolor import cprint
import asyncio

if __name__ == "__main__":

    cprint(TITLE, TITLE_COLOR)
    cprint(f'\ncreared by https://t.me/hodlmodeth & https://github.com/polypox', TITLE_COLOR)


    MODULE = int(input('''
MODULE:
1.  ultra
2.  mint + bridge
3.  mint
4.  bridge
5.  check nfts
6.  refuel                       

Выберите модуль (1 - 6) : '''))

    asyncio.run(main(MODULE))


