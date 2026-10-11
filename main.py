import logging
from src.extract import extract_prices
from src.transform import transform_prices
from src.load import load_prices

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s ")

def main():
    raw = extract_prices()
    df = transform_prices(raw)
    load_prices(df)

if __name__ == "__main__":
    main()