-- Daily grain now (was weekly, keyed off fuel price updates). Every
-- calendar day gets a value for every indicator via forward-fill —
-- weekends included, since exchange_rate needed a continuous spine.
-- `month` is kept as a convenience column for easy grouping in Power BI.

select
    spine.date,
    date_trunc('month', spine.date)::date as month,
    fuel.ron95,
    fuel.ron97,
    fuel.diesel,
    fuel.ron95_skps,
    fuel.diesel_budi,
    fuel.diesel_skds,
    fuel.ron95_budi95,
    fuel.diesel_eastmsia,
    cpi.cpi_index,
    exchange.usd,
    exchange.sgd,
    exchange.eur,
    exchange.gbp,
    exchange.jpy,
    opr.new_opr_level
from {{ ref('date_spine') }} as spine
left join {{ ref('int_fuel_daily_filled') }} as fuel
    on spine.date = fuel.date
left join {{ ref('int_cpi_daily_filled') }} as cpi
    on spine.date = cpi.date
left join {{ ref('int_exchange_daily_filled') }} as exchange
    on spine.date = exchange.date
left join {{ ref('int_opr_daily_filled') }} as opr
    on spine.date = opr.date
order by spine.date
