# Copyright [2022-2027] Şefik Efe Altınoluk
#
# This file is a part of project libarbitrage©
# For more details, see https://github.com/f4T1H21/Arbitrage-Bot-Code-Library
#
# Licensed under the GNU GENERAL PUBLIC LICENSE Version 3.0 (the "License")
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.gnu.org/licenses/gpl-3.0.html


"""An extensible library allows to analyze DEX-to-DEX arbitrage oportunities autonomously, besides advanced decentralized exchange operations"""

from sys import exit as sysexit
from json import loads as jsonloads, dumps as jsondumps
from math import perm
from threading import Thread

from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError

from time import sleep, strftime, localtime
from web3 import Web3, HTTPProvider as web3_HTTPProvider, exceptions as web3_exceptions


class c:
    """
    Color class
    """
    show = '\033[?25h' # Show cursor
    hide = '\033[?25l' # Hide cursor
    default = '\033[0m'# Default color

    underline = '\033[4;4m'

    # Foreground colors
    black ='\033[1;90m'
    red ='\033[1;91m'
    green ='\033[1;92m'
    yellow ='\033[1;93m'
    blue ='\033[1;94m'
    purple='\033[1;95m'
    cyan ='\033[1;96m'
    white ='\033[1;97m'

    # Background colors
    b_black ='\033[0;100m'
    b_red ='\033[0;101m'
    b_green ='\033[0;102m'
    b_yellow ='\033[0;103m'
    b_blue ='\033[0;104m'
    b_purple='\033[0;105m'
    b_cyan ='\033[0;106m'
    b_white ='\033[0;107m'


def printHeader(hangisi):
        info = f"""
{c.blue}[{c.white}i{c.blue}] Info: {c.white}Currencies are in format of {c.purple}USD{c.default}
{c.red}[{c.white}!{c.red}] Warning: {c.white}This program assumes {c.purple}USDT{c.white} as {c.purple}USD{c.white}!{c.default}
"""
        headers = """
┌─────────┬────────────────────┬──────────┬──────────┬─────┬─────┬──────────────────────┬───────────────────┐
│BLOCK NUM│LOCAL TIMESTAMP     │DEX1      │DEX2      │SELL │BUY  │UNIT REVENUE          │THRESHOLD AMOUNT   │
├─────────┼────────────────────┼──────────┼──────────┼─────┼─────┼──────────────────────┼───────────────────┤"""
        if hangisi == 'info':
            print(info)
        elif hangisi == 'headers':
            print(headers)
        elif hangisi == 'both':
            print(info + headers)


def writeRow(*tuples): # Create and print a row (to be placed in a table).
    row = ""
    for item in tuples:
        word = str(item[0])
        size = 15
        add_zeros = False
        try:
            size = item[1]
            add_zeros = eval(item[2])
        except:
            pass
        # if len(item) == 2:
        #     size = item[1]
        if add_zeros:
            word += ''.join('0' for i in range(size-1 - len(str(word))))
        row += f"│{word}"
        fill = 0
        fill = size - len(word)
        for i in range(fill):
            row += " "
    row += "│"
    print(row)


def printFormattedData(liste:list) -> None:
    """
    Apply 'writeRow' function to every item in a given list consisting of dictionaries.
    """

    try:
        if INTERACTIVE == False:
            printHeader('headers')
    except NameError:
        printHeader('headers')
            
    for girdi in liste:
        writeRow((girdi.get('blocknum'), 9),\
            (strftime('%Y-%m-%d %H:%M:%S', localtime(girdi.get('timestamp'))), 20),\
            (girdi.get('dex1'), 10),\
            (girdi.get('dex2'),10),\
            (girdi.get('sell_token'),5),\
            (girdi.get('buy_token'),5),\
            (girdi.get('revenue_per_1usd'), 22, 'True'),\
            (girdi.get('minimum_amount'), 19, 'True')\
        )
    print('├─────────┼────────────────────┼──────────┼──────────┼─────┼─────┼──────────────────────┼───────────────────┤')


def animate(sentence:str, condition:str, interactive:bool, mode=None) -> None:
    """
    Till the given condition becomes 'True', delay,
    meanwhile print an animation if the program is interactive.

    Not: Cümle olarak verilen yazının karakter sayısının eğer msfconsole modu
    seçildiyse 4'ün normal mod (None) seçildiyse 8'in katları olması gerekiyor.
    """
    signs = ['|', '/', '─', '\\'] # Msfconsole'daki gibi :)
    signs_2 = ['└', '├', '┌', '┬', '┐', '┤', '┘', '┴' ]
    index = 0
    while not eval(condition):
        if interactive:
            for sign in signs_2:
                if mode == 'msfconsole':
                    if (lstindex:=signs_2.index(sign)) >= len(signs):
                        lstindex = lstindex - 4
                    sign = signs[lstindex]
                char = sentence[index] # Büyüklük/küçüklük durumu değiştirilecek olan karakter
                text = f"{c.purple}[{c.yellow}{sign}{c.purple}] {c.white}{sentence[0:index]}{c.blue}{char.swapcase()}{c.white}{sentence[index+1:]}{c.default}       "
                print(text, end="\r") # end='\r' ile imleci yazıyı yazdığın satırın başında bırakıyorsun.
                sleep(.1)

                index += 1
                if index == len(sentence):
                    if mode == 'msfconsole':
                        array = signs
                    else:
                        array = signs_2
                    for i in range(len(array)):
                        print(f"{c.purple}[{c.yellow}{array[i]}{c.purple}] {c.white}{sentence}{'.' * (i-1)}{c.blue}{'•' if i >= 1 else ''}{c.default}", end="\r")
                        sleep(.1)
                    for i in range(2 if mode == 'msfconsole' else 1):
                        for sign in array:
                            print(f"{c.purple}[{c.yellow}{sign}{c.purple}] {c.white}{sentence}{'.' * 3 if mode == 'msfconsole' else '.' * 7}{c.default}", end="\r")
                            sleep(.1)
                    index = 0
        else:
            pass

    if interactive:
        print(f"{c.purple}[👌] {c.white}{sentence}... {c.green}Done{c.default}")


class Block: # Get transaction datas of the latest block in the specified blockchain network via Infura API.
    def __init__(self, APIKEY:str, network:str=None, w3:object=None):
        if type(w3) is not type(None):
            self.w3 = w3
        elif network == 'ropsten':
            self.w3 = Web3(web3_HTTPProvider(f'https://ropsten.infura.io/v3/{APIKEY}')) # Ropsten network node servisi
        elif network == 'mainnet':
            self.w3 = Web3(web3_HTTPProvider(f'https://mainnet.infura.io/v3/{APIKEY}')) # Main network node servisi
        else:
            raise Exception("Specify a web3 http node or choose network: 'ropsten', 'mainnet'")

        while True:
            try:
                block = self.w3.eth.get_block('latest', True)
            except web3_exceptions.BlockNotFound:
                continue

            self.txs = block['transactions']
            self.number = block['number']
            self.timestamp = block['timestamp']

            if len(self.txs) != 0:
                break


    def calculateAvgTxFee(self) -> float:
        """
        Average up the transaction fees of every transaction in the block.
        """
        transaction_fees = []
        for tx in self.txs:
            # wei cinsinden değerler alınır | 1 wei = 10^-18 ETH
            gas_price = tx['gasPrice']
            gas_used = self.w3.eth.waitForTransactionReceipt(tx['hash'])['gasUsed']
            # Transaction fee = gas_price * gas_used * 10^-18
            transaction_fees.append(float(f"{gas_price * gas_used * (10**-18):.18f}"))

        avg_fee = sum(transaction_fees) / len(transaction_fees)
        return avg_fee # Return type: ETH


    def calculateMyGasPrice(self) -> int:
        """
        Average up the gas prices of every transaction and return %110 of it.
        
        In blockchain, there's a high chance for the transaction to be written
        at the next block if you give %10 more than the previous block's
        average gas price as your gas price to the next block.
        """
        prices = [tx['gasPrice'] for tx in self.txs]
        avg_gp = int(sum(prices) / len(prices))
        my_gp = int(avg_gp + (avg_gp/10)) # GasPrice + GasPrice * %10
        return my_gp # Return type: wei



class AmountError(Exception): # Custom 'Exception' object
    pass


class Prices: # Decentralized Exchange Operations
    def __init__(self, chosen_dexes:list, chosen_tokens:list, operation:str, interactive:bool) -> None:
        self.INTERACTIVE = interactive
        available_tokens = {
            'eth': {'address': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'decimals': 18}, # WETH
            'btc': {'address': '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599', 'decimals': 8},  # WBTC
            'ftt': {'address': '0x50D1c9771902476076eCFc8B2A83Ad6b9355a4c9', 'decimals': 18},  # FTX Token
            'aave': {'address': '0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9', 'decimals': 18},
            'link': {'address': '0x514910771AF9Ca656af840dff83E8264EcF986CA', 'decimals': 18}, # ChainLink    
            
            'usdt': {'address': '0xdAC17F958D2ee523a2206206994597C13D831ec7', 'decimals': 6},  # Stable
            'usdc': {'address': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 'decimals': 6},  # Stable
            'cels': {'address': '0xaaAEBE6Fe48E54f431b0C390CfaF0b017d09D42d', 'decimals': 4}   #Celsius # Patladı
            }

        available_dexes = {
            'uniswap': 'Uniswap_V3',
            'sushiswap': 'SushiSwap'
        }

        if chosen_tokens == 'all':
            chosen_tokens = available_tokens.keys()

        # string cinsinden 1 tane VEYA listedeki bütün ögelerin available listesinde olmadığı durumda verilecek olan hata
        if not all(x in available_tokens.keys() for x in tuple(chosen_tokens)):
            raise ValueError(f"Invalid value for 'tokens', can only specify following tokens {c.underline}in list format{c.default}: {', '.join(i for i in available_tokens.keys())} ")
        if not all(x in available_dexes.keys() for x in tuple(chosen_dexes)):
            raise ValueError(f"Invalid value for 'dexes', can only specify following dexes {c.underline}in list format{c.default}: {', '.join(i for i in available_dexes.keys())} ")

        self.tokens = {key:value for key, value in available_tokens.items() if key in set(chosen_tokens) | {'usdt'}}
        self.dexes = {key:value for key, value in available_dexes.items() if key in set(chosen_dexes)}

        # Yeterli sayıda olmadıklarında verilecek olan hata 
        if len(self.tokens) < 2:
            raise AmountError(f"Invalid amount of 'tokens', specify an a number of at least {c.underline}2 different{c.default} ERC-20 tokens!")
        if len(self.dexes) != 2:
            raise AmountError(f"Invalid amount of 'exchanges', specify an exact number of {c.underline}2 different{c.default} exchanges!")

        # Bütün swap fiyatlarının içerisinde tutulacağı nesne
        self.prices_dict = {k:{} for k in self.dexes.keys()}
        self.token_pairs = self.generatePermutations(self.tokens.keys())
        
        self.threads = {
            f"{dex[0]}_{pair}":f"Thread(daemon=True, target=self.updatePrices, args=('{dex}', '{operation}', '{pair}', 1))"\
            for pair in self.token_pairs\
            for dex in self.dexes.keys()
        }
        self.parent_threads = {
            f"parent_{thread_name}":f"{thread_content.replace('updatePrices', 'handleThreads')}"\
            for thread_name, thread_content in self.threads.items()
        }
        
        # İlk durumda token sayısının ikili permütasyonundan oluşan fakat fiyat almada hata meydana geldikçe azaltılan
        # ve asıl amacı arbitraj nesnesinin kullanımına sunulmak üzere hata vermeyen bütün fiyat çiftlerinin içinde tutulduğu 
        # nesneye eklenip eklenilmediği koşulunun kontrolü sırasında kullanılmak olan değişken.

        # Çünkü arbitraj hesaplamaları uygun olan bütün çiftlerin fiyatları bir değişkenin içerisinde hazır olmadan başlatılamaz.
        self.available_swap_liquidity_number = perm(len(self.tokens.keys()), 2)
        # Fiyatını alırken yetersiz likidite hatası gibi hata meydana gelen çiftlerin dex-token_pair:hata_mesajı formatında yer alacağı nesne.
        self.failed_pairs = dict()


    # Return swap price for the given token pair according to;
    # - DEX name (uniswap, sushiswap, etc...)
    # - Amount of the token to be swapped
    # - Buy/Sell price. 
    def getDexPrice(self, dex:str, op:str, token_pair:str, amount:float) -> float:
        # eth_usdt -> eth:buy, usdt:sell | 1 eth satın almak için kaç usdt satmalıyım? -> 1280
        # eth_usdt -> eth:sell, usdt:buy | 1 eth satarak kaç usdt alabilirim? -> 1280
        # Cevaplar aynı.

        if op == 'buy':
            buyToken = token_pair.split('_')[0]
            sellToken = token_pair.split('_')[1]
            decimals = self.tokens.get(buyToken).get('decimals')
        elif op == 'sell':
            buyToken = token_pair.split('_')[1]
            sellToken = token_pair.split('_')[0]
            decimals = self.tokens.get(sellToken).get('decimals')

        amount = amount * (10**decimals)
        query = {
            'buyToken': self.tokens.get(buyToken).get('address'),
            'sellToken': self.tokens.get(sellToken).get('address'),
            'includedSources': dex,
            f'{op}Amount': amount
        }

        url = f"https://api.0x.org/swap/v1/price?{urlencode(query)}"
        status = 0
        while status != 200:
            try:
                response = urlopen(url, timeout=10)
                status = response.code

            except HTTPError as err:
                if err.code == 429: # HTTP 'Too many requests' durum kodu
                    sleep(.5)
                elif err.code == 400: # API'a özel, genelde 'insufficient asset liquiditiy' hataları
                    http_body = jsonloads(err.read())
                    error_msg = http_body['validationErrors'][0]['reason'].capitalize().replace('_', ' ')
                    sleep(10)
                    if self.INTERACTIVE:
                        print(f"{c.b_red}[E]{c.default} {c.red}{error_msg}{c.white} for {c.cyan}{token_pair}{c.white} token pair on {c.cyan}{dex}{c.white} exchange!{c.default}")
                    self.failed_pairs.update({f"{dex}-{token_pair}":error_msg})
                    exit()
                else:
                    print(err)

            except URLError as err:
                if str(err.reason) == '[Errno -3] Temporary failure in name resolution':
                    print("Error: Failure in name resolution, check your internet connection!")
                    sleep(5)
                else:
                    print(err)

        response_json = jsonloads(response.read())
        #print(jsondumps(response_json, indent=4, sort_keys=True)) # Debug: Print unparsed response as json, directly.
        return response_json['price']


    def updatePrices(self, dex, op, token_pair, amount):
        # Handle http/ssl errors
        #try:
        price = self.getDexPrice(self.dexes.get(dex), op, token_pair, amount)
        self.prices_dict.get(dex).update({token_pair:price})
        # except Exception as e:
        #     print('An error occured in updating prices_dict at an instance of Prices class:\n' + str(e))
        #     sysexit()


    def handleThreads(self, dex, op, token_pair, amount):
        thread_name = f"{dex[0]}_{token_pair}"
        # Pairin tersini ve pairi kontrol etmemizin sebebi eğer insufficient vb. bir hata ile karşılaşırsak
        # çiftlerin tersleriyle alakalı threadleri sonlandırıyoruz çünkü fiyat verisi onlar için de alınamıyor.
        pairin_tersi = f"{''.join(self.dexes.get(i) for i in self.dexes.keys() if i != dex)}-{token_pair.split('_')[1]}_{token_pair.split('_')[0]}"
        pair_ve_tersi = [f"{self.dexes.get(dex)}-{token_pair}", pairin_tersi]
        # Geçerli pair veya tersinin diğer borsadaki threadinde bir hata çıkmadığı sürece thread döngüsünü çalıştır. 
        while not any(x in self.failed_pairs.keys() for x in pair_ve_tersi):
            exec(f"{thread_name} = {self.threads.get(thread_name)}")
            eval(thread_name).start()
            eval(thread_name).join() # Wait until current thread ends with either success or http(conn reset)/ssl error.
        # Arbitraj hesabı için hem bu paire hem de diğer borsada bu pairin tersine bakmamız gerektiği için 0.5 çıkarıyoruz.
        # Çünkü tek bir arbitrage işlemini yapmamızı sağlayan bu fonksiyonun ait olduğu threadin pairi ve o pairin tersinin threadi.
        self.available_swap_liquidity_number -= 0.5 # Remove current pair from available liquidities
        if token_pair in self.prices_dict.get(dex).keys():
            del self.prices_dict.get(dex)[token_pair]

    @classmethod
    def generatePermutations(cls, liste:list) -> list:
        """
        Create a list of given items' binary permutations without theirselves.
        """
        permutations = []
        for item in liste:
            other_items = (name for name in liste if name != item)
            # Listenin güncellenen bir yapı olmasının sebebi:
            # Eğer ikili kombinasyonlarını alsaydık, öge eklenirken hâlihazırda (tersi) var mı diye bakmalıydık.
            # Aşağıdaki satırın devamındaki yorumu kaldırırsam eğer permütasyon değil kombinasyon yapmış oluyorum.
            permutations = permutations + [f"{item}_{name}" for name in other_items]# if f"{name}_{item}" not in (pair for pair in permutations)]
        return permutations


    def runThreads(self) -> None: # Run price threads asynchronously
        for thread_name, thread in self.parent_threads.items():
            exec(f"{thread_name} = {thread}")
            eval(thread_name).start()
            sleep(.3) # Beklememin sebebi http isteklerinin üst üste gitmesini engellemektir.


    def waitUntilAll(self): # Wait until all the available prices are placed to the dictionary for every token.
        # Eleman sayısını kontrol et: Permütasyon
        if not (len(self.prices_dict.get('uniswap')) == len(self.prices_dict.get('sushiswap')) == self.available_swap_liquidity_number):
            return False
        else:
            return True



class TxFee: # TxFee processes
    def __init__(self, apikey):
        self.APIKEY = apikey

    def runThread(self): # Run an independent thread for 'getTxFee' function.
        fee_thread = Thread(daemon=True, target=self.getTxFee)
        fee_thread.start()

    # Convert txfees to usd via getting the price data from an instance of 'Price' object and using the 'exchange' function of 'Arbitrage' class.
    def getTxFee(self): 
        while True:
            block = Block(self.APIKEY, network='mainnet')
            self.timestamp = block.timestamp
            ethFee = block.calculateAvgTxFee() # In format of ETH
            self.usdFee = Arbitrage.exchange(price_obj.prices_dict, 'uniswap', 'eth', 'usdt', ethFee)
            self.number = block.number # Bunu en son almak önemli, çünkü waituntilnextblock fonksiyonunda, fee için de bunu kontrol ediyoruz.
            sleep(.01)

    # Unless current block's blocknumber is not equal to the given number, return False.
    def waitUntilNextBlock(self, eski=None):
        if eski == None:
            if not 'number' in vars(self).keys():
                return False
            else:
                return True
        while eski == self.number: # Preassume that, the previous fee can not be the same as the next fee. Bkz, Blok hatası in GasPrice_Explorer.
            pass




class Arbitrage: # swap, exchange, data output and arbitrage analyze operations
    def __init__(self, kar_oranı, interactive):
        self.INTERACTIVE = interactive
        self.arbitrage_data = dict()
        self.temp_values_list = list()
        self.key_templates = ("blocknum", "timestamp", "dex1", "dex2", "sell_token", "buy_token", "revenue_per_1usd", "minimum_amount")
        if self.INTERACTIVE:
            self.kar_oranı = self.getKarOranı()
            print(c.hide) # İmleci gizle, hide pointer
        else:
            self.kar_oranı = kar_oranı


    def getKarOranı(self):
        kar_oranı = input(f'{c.cyan}=> {c.white}Enter minimum earning rate in percentage (blank for all positives): {c.cyan}%')
        if kar_oranı == "":
            kar_oranı = 0 # Verbose, write all the positive ones
        kar_oranı = float(kar_oranı)
        return kar_oranı


    @classmethod
    def exchange(cls, kur:dict, exchange_name:str, sell_token:str, buy_token:str, amount:float) -> float: # Exchange tokens
        buy_price = float(kur.get(exchange_name).get(f"{sell_token}_{buy_token}"))
        summary = buy_price * amount
        return summary


    def swap_tokens(self, kur, dex1, dex2, token1, token2): # Apply the swaps
        if token1 == 'usdt': # base_amount ve normal_price işlemlerinde usdt -> usdt olamayacağı için...
            exit()
        # 1 doların token cinsinden satış fiyatı nedir?
        base_amount = self.exchange(kur, dex1, 'usdt', token1, 1)

        # Bir dolara alınan tokenın satış fiyatı, kaç dolar?
        normal_price = self.exchange(kur, dex1, token1, 'usdt', base_amount)

        # Swap between DEXes
        x = self.exchange(kur, dex1, token1, token2, base_amount)
        y = self.exchange(kur, dex2, token2, token1, x)
        final_purse = self.exchange(kur, dex1, token1, 'usdt', y)

        return final_purse, normal_price


    def analyze(self, fee, kur, metadata, dex1, dex2, sell_token, buy_token): # Check if arbitrage exists in compliance with the minimum revenue
        final, normal = self.swap_tokens(kur, dex1, dex2, sell_token, buy_token)
        if final > normal:
            revenue_per_1usd = final - normal # Birim kazanç
            minimum_amount = fee / revenue_per_1usd # Fee'yi karşılamak için en az kaç dolarlık işlem yapılmalı?
            if revenue_per_1usd >= (self.kar_oranı / 100):
                blocknum = metadata[0]
                timestamp = metadata[1]
                data = (blocknum, timestamp, dex1, dex2, sell_token, buy_token, revenue_per_1usd, minimum_amount)
                self.temp_values_list.append(data)


    def processThreads(self, threads): # Start every arbitrage thread and wait till all to finish.
        for thread_name, thread in threads.items():
            exec(f"{thread_name} = {thread}")
            eval(thread_name).start()
        for thread_name, thread in threads.items():
            eval(thread_name).join()


    def loop(self, fee_obj:object, price_obj:object): # The main loop that organizes all the arbitrage process using the functions of of this class.
        while True:
            current_fee = fee_obj.usdFee
            current_prices = price_obj.prices_dict
            current_metadata = (fee_obj.number, fee_obj.timestamp)

            threads = {
                f"arbitrageOf_{dex[0]}_{pair}":
                f"Thread(daemon=True, target=self.analyze, args=({current_fee}, {current_prices}, {current_metadata}, '{dex}', '{[i for i in price_obj.dexes.keys() if i != dex][0]}', '{pair.split('_')[0]}', '{pair.split('_')[1]}'))" \
                        for pair in price_obj.token_pairs
                        for dex in price_obj.dexes.keys()
                        if pair in price_obj.prices_dict.get(dex)
            }


            self.processThreads(threads)
            self.arbitrage_data.update({current_metadata[0]:[dict(zip(self.key_templates, values)) for values in self.temp_values_list]})
            self.temp_values_list.clear()
            if self.INTERACTIVE:
                printFormattedData(self.arbitrage_data.get(current_metadata[0]))
            fee_obj.waitUntilNextBlock(current_metadata[0])



def getArbitrageData() -> dict:
    return arbitrage_obj.arbitrage_data


def arbitrage(APIKEY:str, exchanges:list=['uniswap', 'sushiswap'], tokens:list='all', operation:str='sell', min_revenue:float=0, interactive:bool=False) -> None:
    """
    Initialize objects of the classes and check for arbitrage in compliance with the given parameters.

    ---
    :APIKEY: Your Infura APIKEY
    
    :exchanges: A list including two of the available exchanges
    
    :tokens: A list including at least one available token apart from "usdt"
    
    *operation* A string indicating the basic price type while analyzing the exchanges
    
    *min_revenue* A floating point number indicating the minimum profit rate percent
    
    *interactive* A boolean, setting this as True will bring animations and a real-time monitor to your screen.
    ---
    
    Available exchanges: ['uniswap', 'sushiswap']
    Available tokens: ['eth', 'btc', 'ftt', 'aave', 'link', 'usdt', 'usdc', 'cels']
    """

    global arbitrage_obj, price_obj, fee_obj, INTERACTIVE

    try:
        INTERACTIVE = interactive
        price_obj = Prices(exchanges, tokens, operation=operation, interactive=interactive)
        arbitrage_obj = Arbitrage(kar_oranı=min_revenue, interactive=interactive)
        fee_obj = TxFee(APIKEY)

        Thread(daemon=True, target=price_obj.runThreads).start()

        # Önce kurun beklenmesi önemli, çünkü fee formatını çevirme için de kur kullanılıyor.
        animate("Initializing exchange prices", 'price_obj.waitUntilAll()', mode='msfconsole', interactive=interactive)
        fee_obj.runThread()
        animate("Getting latest block information", 'fee_obj.waitUntilNextBlock()', interactive=interactive)

        if interactive:
            printHeader('both')
            arbitrage_obj.loop(fee_obj, price_obj)
        else:
            Thread(daemon=True, target=arbitrage_obj.loop, args=(fee_obj, price_obj)).start()
            sleep(2) # Sleep until the first loop finishes and the dictionary fills up with the initial datas

    except KeyboardInterrupt:
        exitmsg = None
        if interactive:
            exitmsg = f"\n    {c.green}Program exited!"
        sysexit(exitmsg)
    # except Exception as e:
    #     sysexit(f"\nError: {e}")
    finally:
        if interactive:
            print(c.show)
