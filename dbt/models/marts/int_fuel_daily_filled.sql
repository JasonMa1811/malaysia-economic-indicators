-- Fuel prices only change on Thursdays. Forward-fill onto every day
-- until the next Thursday update — "what was the price in effect
-- on this day", not "was there an announcement this day".
--
-- All fuel columns come from one weekly source row, so they're
-- null/non-null together — one fill_group (driven by ron95) covers all.

with joined as (
    select
        spine.date,
        fuel.ron95,
        fuel.ron97,
        fuel.diesel,
        fuel.ron95_skps,
        fuel.diesel_budi,
        fuel.diesel_skds,
        fuel.ron95_budi95,
        fuel.diesel_eastmsia
    from {{ ref('date_spine') }} as spine
    left join {{ ref('stg_fuelprice') }} as fuel
        on spine.date = fuel.date
),

grouped as (
    select
        *,
        count(ron95) over (order by date) as fill_group
    from joined
)

select
    date,
    first_value(ron95) over (partition by fill_group order by date) as ron95,
    first_value(ron97) over (partition by fill_group order by date) as ron97,
    first_value(diesel) over (partition by fill_group order by date) as diesel,
    first_value(ron95_skps) over (partition by fill_group order by date) as ron95_skps,
    first_value(diesel_budi) over (partition by fill_group order by date) as diesel_budi,
    first_value(diesel_skds) over (partition by fill_group order by date) as diesel_skds,
    first_value(ron95_budi95) over (partition by fill_group order by date) as ron95_budi95,
    first_value(diesel_eastmsia) over (partition by fill_group order by date) as diesel_eastmsia
from grouped
