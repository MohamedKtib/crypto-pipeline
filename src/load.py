import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
log = logging.getLogger(__name__)

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS crypto_prices (
    id SERIAL PRIMARY KEY,
    coin_id TEXT NOT NULL,
    symbol TEXT,
    name TEXT,
    current_price NUMERIC,
    market_cap NUMERIC,
    total_volume NUMERIC,
    high_24h NUMERIC,
    low_24h NUMERIC,
    price_range_24h NUMERIC,
    last_updated TIMESTAMPTZ NOT NULL,
    fetched_at TIMESTAMPTZ NOT NULL,
    UNIQUE (coin_id, last_updated)
);
"""

INSERT = """
INSERT INTO crypto_prices
    (coin_id, symbol, name, current_price, market_cap, total_volume,
     high_24h, low_24h, price_range_24h, last_updated, fetched_at)
VALUES
    (:coin_id, :symbol, :name, :current_price, :market_cap, :total_volume,
     :high_24h, :low_24h, :price_range_24h, :last_updated, :fetched_at)
ON CONFLICT (coin_id, last_updated) DO NOTHING;
"""

def load_prices(df):
    engine = create_engine(os.getenv("DB_URL"))
    df = df.astype(object).where(df.notna(), None)  # NaN -> NULL
    records = df.to_dict(orient="records")

    with engine.begin() as conn:
        conn.execute(text(CREATE_TABLE))
        conn.execute(text(INSERT), records)

    log.info("Processed %d rows", len(records))