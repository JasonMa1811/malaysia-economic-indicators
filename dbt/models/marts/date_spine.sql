-- Continuous calendar, one row per day, including weekends that
-- raw.exchange_rate itself has no rows for (markets closed Sat/Sun).
-- This is now the driving grain for the whole marts layer.

select
    generate_series(
        (select min(date) from {{ ref('stg_exchange_rate') }}),
        (select max(date) from {{ ref('stg_exchange_rate') }}),
        interval '1 day'
    )::date as date
