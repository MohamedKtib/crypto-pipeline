from src.transform import transform_prices

def make_coin(**overrides):
    coin = {
        "id": "bitcoin", "symbol": "btc", "name": "Bitcoin",
        "current_price": 100.0, "market_cap": 1000, "total_volume": 500,
        "high_24h": 110.0, "low_24h": 90.0,
        "last_updated": "2026-10-11T10:00:00.000Z",
    }
    coin.update(overrides)
    return coin

def test_symbol_is_uppercase():
    df = transform_prices([make_coin()])
    assert df.loc[0, "symbol"] == "BTC"

def test_invalid_price_is_removed():
    df = transform_prices([make_coin(), make_coin(id="bad", current_price=-5)])
    assert list(df["coin_id"]) == ["bitcoin"]

def test_missing_price_is_removed():
    df = transform_prices([make_coin(), make_coin(id="empty", current_price=None)])
    assert len(df) == 1


def test_duplicates_are_removed():
    df = transform_prices([make_coin(), make_coin()])
    assert len(df) == 1


def test_price_range():
    df = transform_prices([make_coin()])
    assert df.loc[0, "price_range_24h"] == 20.0