CREATE TABLE IF NOT EXISTS market.market_sessions (
    id BIGSERIAL PRIMARY KEY,
    exchange_id BIGINT NOT NULL
        REFERENCES market.exchanges(id)
        ON DELETE CASCADE,
    session_date DATE NOT NULL,
    market_open TIMESTAMPTZ NOT NULL,
    market_close TIMESTAMPTZ NOT NULL,
    is_trading_day BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_market_session_exchange_date
        UNIQUE (exchange_id, session_date),

    CONSTRAINT chk_market_session_times
        CHECK (market_close > market_open)
);

CREATE INDEX IF NOT EXISTS idx_market_sessions_exchange_date
    ON market.market_sessions(exchange_id, session_date DESC);

ALTER TABLE market.instruments
    ADD COLUMN IF NOT EXISTS exchange_symbol VARCHAR(100);

ALTER TABLE market.instruments
    ADD COLUMN IF NOT EXISTS trading_symbol VARCHAR(100);

ALTER TABLE market.instruments
    ADD COLUMN IF NOT EXISTS isin VARCHAR(20);

ALTER TABLE market.instruments
    ADD COLUMN IF NOT EXISTS sector VARCHAR(150);

ALTER TABLE market.instruments
    ADD COLUMN IF NOT EXISTS industry VARCHAR(150);

CREATE INDEX IF NOT EXISTS idx_market_instruments_exchange_symbol
    ON market.instruments(exchange_symbol);

CREATE INDEX IF NOT EXISTS idx_market_instruments_isin
    ON market.instruments(isin);
