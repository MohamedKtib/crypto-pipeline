import logging
import requests

log = logging.getLogger(__name__)
URL = "https://api.coingecko.com/api/v3/coins/markets"

def extract_prices(currency="usd", per_page=20):
    log.info("Fetching top %d coins", per_page)
    params = {
        "vs_currency": currency,
        "order": "market_cap_desc",
        "per_page": per_page,
        "page":1,
    }
    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()