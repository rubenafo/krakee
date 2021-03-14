import logging as logger

"""
Pretty names for common asset altnames
"""
PRETTY_NAMES = {
    'AAVE': 'Aave',
    'ADA': "Cardano",
    'ALGO': 'Algorand',
    'ANT': 'Aragon',
    'ATOM':'Cosmos',
    "ATOMS.S":"",
    "BAL":"Balancer",
    "BAT":"Basic Attention Token",
    "BCH": "Bitcoin Cash",
    "CHF":"Swiss franc",
    "COMP":"Compound",
    "CRV":"Curve",
    "DAI":"Dai",
    "DASH":"Dash",
    "DOT":"Polkadot",
    "DOT.S":"Polkadot",
    "EOS":"EOS",
    "ETH2":"Ethereum 2",
    "ETH2.S":"Ethereum 2",
    "EUR.HOLD":"Euro",
    "EUR.M":"Euro",
    "EWT":"Energy Web Token",
    "FIL":"Filecoin",
    "FLOW":"Flow",
    "FLOW.S":"Flow",
    "FLOWH": "Flow",
    "FLOWH.S":"Flow",
    "GNO":"Gnosis",
    "GRT":"The Graph",
    "ICX":"ICON",
    "KAVA":"Kava",
    "KAVA.S":"Kava",
    "KEEP":"Keep",
    "FEE":"Kraken Fee Credits",
    "KNC":"Kyber Network",
    "KSM":"Kusama",
    "KSM.S":"Kusama",
    "LINK":"Link",
    "LSK":"Lisk",
    "MANA":"Decentraland",
    "NANO":"Nano",
    "OCEAN":"Ocean",
    "OMG":"OmiseGO",
    "OXT":"Orchid",
    "PAXG":"PAX Gold",
    "QTUM":"QTUM",
    "REPV2":"Augur v2",
    "SC":"Siacoin",
    "SNX":"Synthetix",
    "STORJ":"Storj",
    "TBTC":"tBTC",
    "TRX":"Tron",
    "UNI":"Uniswap",
    "USD.HOLD":"US Dollar",
    "USD.M":"US Dollar",
    "USDC":"USD Coin",
    "USDT":"Tether",
    "WAVES":"Waves",
    "XBT.M":"Bitcoin",
    "ETC":"Ethereum Classic",
    "ETH":"Ethereum",
    "LTC":"Litecoin",
    "MLN":"Melon",
    "REP":"Augur",
    "XTZ":"Tezos",
    "XTZ.S":"Tezos",
    "XBT":"Bitcoin",
    "XDG":"Dogecoin",
    "XLM":"Stellar Lumens",
    "XXLM": "Stellar Lumens",
    "XMR":"Monero",
    "XRP":"Ripple",
    "ZEC":"Zcash",
    "YFI":"Yearn Finance",
    "AUD":"Australian Dollar",
    "CAD":"Canadian Dollar",
    "EUR":"Euro",
    "GBP":"Great British Pound",
    "JPY":"Japan Yen",
    "USD":"US Dollar"
}

"""
Returns the human-friendly version of the ticker.
The input ticker name is returned if there is no match in the list.
"""
def get_pretty_name(alt_name_raw:str):
    alt_name = str.upper(alt_name_raw)
    if alt_name.startswith("XX"):
        alt_name = alt_name[1:]
    if alt_name in PRETTY_NAMES:
        return PRETTY_NAMES[alt_name]
    else:
        logger.warn("PrettyNames: {} mapping not found".format(alt_name))
        return alt_name