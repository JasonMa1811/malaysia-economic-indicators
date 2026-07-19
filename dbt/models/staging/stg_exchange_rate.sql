-- Mirrors etl/transform/transform.py::transform_exchange_rate()
-- BNM publishes buying/selling/middle quotes per currency per day —
-- keep only 'middle' (the standard reference rate), drop rate_type.

select
    date::date as date,
    usd,
    sgd,
    eur,
    gbp,
    jpy,
    aed,
    aud,
    bnd,
    cad,
    chf,
    cny,
    egp,
    hkd,
    idr,
    inr,
    khr,
    krw,
    mmk,
    npr,
    nzd,
    php,
    pkr,
    sar,
    thb,
    twd,
    vnd,
    xdr
from {{ source('raw', 'exchange_rate') }}
where rate_type = 'middle'
