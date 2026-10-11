import logging
from datetime import datetime, timezone
import pandas as pd

log = logging.getLogger(__name__)

COLUMNS = ["id", "symbol", "name", "current_price", "market_cap", "total_volume", "high_24h", "low_24h", "last_updated",]

def transform_prices(raw):
    df = pd.DataFrame(raw)[COLUMNS]
    df = df.rename(columns={"id" : "coin_id"})

    df["symbol"] = df["symbol"].str.upper()
    df["last_updated"] = pd.to_datetime(df["last_updated"])
    df["fetched_at"] = datetime.now(timezone.utc)

    df = df.dropna(subset=["coin_id", "current_price"])
    df = df.drop_duplicates(subset=["coin_id", "last_updated"])

    df["price_range_24h"] = df["high_24h"] - df["low_24h"]

    # data quality check : prices must be positive
    bad = df[df["current_price"] <= 0 ]
    if not bad.empty:
        log.warning("Dropping %d rows with invalid price", len(bad))
    df = df[df["current_price"] > 0]
    
    return df