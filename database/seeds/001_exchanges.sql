INSERT INTO market.exchanges (code, name, country, timezone)
VALUES
    ('NSE', 'National Stock Exchange of India', 'India', 'Asia/Kolkata'),
    ('BSE', 'BSE Limited', 'India', 'Asia/Kolkata')
ON CONFLICT (code) DO UPDATE
SET
    name = EXCLUDED.name,
    country = EXCLUDED.country,
    timezone = EXCLUDED.timezone;
