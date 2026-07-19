-- Forward-fills exchange rates onto weekends (markets closed, so the
-- "rate" on a Saturday is Friday's close, carried forward — standard
-- practice, not a data quality workaround).
--
-- All 5 currency columns come from one daily source row, so they're
-- null/non-null together — one fill_group (driven by usd) is enough to
-- correctly carry forward every column, not just one.

with joined as (
    select
        spine.date,
        exch.usd,
        exch.sgd,
        exch.eur,
        exch.gbp,
        exch.jpy
    from {{ ref('date_spine') }} as spine
    left join {{ ref('stg_exchange_rate') }} as exch
        on spine.date = exch.date
),

grouped as (
    select
        *,
        count(usd) over (order by date) as fill_group
    from joined
)

select
    date,
    first_value(usd) over (partition by fill_group order by date) as usd,
    first_value(sgd) over (partition by fill_group order by date) as sgd,
    first_value(eur) over (partition by fill_group order by date) as eur,
    first_value(gbp) over (partition by fill_group order by date) as gbp,
    first_value(jpy) over (partition by fill_group order by date) as jpy
from grouped
