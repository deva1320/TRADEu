-- TRADEu Database
-- Migration 002: Market core

CREATE SCHEMA IF NOT EXISTS market;

CREATE TABLE IF NOT EXISTS market.exchanges (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL DEFAULT 'India',
    timezone VARCHAR(64) NOT NULL DEFAULT 'Asia/Kolkata',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS market.instruments (
    id BIGSERIAL PRIMARY KEY,
    exchange_id BIGINT NOT NULL REFERENCES market.exchanges(id),
    symbol VARCHAR(50) NOT NULL,
    name VARCHAR(200),
    instrument_type VARCHAR(50) NOT NULL,
    isin VARCHAR(20),
    currency VARCHAR(10) NOT NULL DEFAULT 'INR',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_market_instrument_exchange_symbol
        UNIQUE (exchange_id, symbol)
);

CREATE INDEX IF NOT EXISTS idx_market_instruments_symbol
    ON market.instruments(symbol);

CREATE INDEX IF NOT EXISTS idx_market_instruments_type
    ON market.instruments(instrument_type);
