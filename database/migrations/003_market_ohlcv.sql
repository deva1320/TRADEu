-- TRADEu Database
-- Migration 003: OHLCV market data

CREATE TABLE IF NOT EXISTS market.ohlcv (
    id BIGSERIAL PRIMARY KEY,

    instrument_id BIGINT NOT NULL
        REFERENCES market.instruments(id)
        ON DELETE CASCADE,

    timeframe VARCHAR(20) NOT NULL,

    candle_time TIMESTAMPTZ NOT NULL,

    open NUMERIC(20,8) NOT NULL,
    high NUMERIC(20,8) NOT NULL,
    low NUMERIC(20,8) NOT NULL,
    close NUMERIC(20,8) NOT NULL,

    volume NUMERIC(30,8),

    source VARCHAR(100) NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_ohlcv_high_low
        CHECK (high >= low),

    CONSTRAINT chk_ohlcv_high_open
        CHECK (high >= open),

    CONSTRAINT chk_ohlcv_high_close
        CHECK (high >= close),

    CONSTRAINT chk_ohlcv_low_open
        CHECK (low <= open),

    CONSTRAINT chk_ohlcv_low_close
        CHECK (low <= close),

    CONSTRAINT uq_market_ohlcv_candle
        UNIQUE (instrument_id, timeframe, candle_time)
);

CREATE INDEX IF NOT EXISTS idx_market_ohlcv_instrument_time
    ON market.ohlcv(instrument_id, candle_time DESC);

CREATE INDEX IF NOT EXISTS idx_market_ohlcv_timeframe_time
    ON market.ohlcv(timeframe, candle_time DESC);
