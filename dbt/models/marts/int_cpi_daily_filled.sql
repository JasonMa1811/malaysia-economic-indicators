-- CPI is published monthly. Forward-fill the overall index onto every
-- day until the next month's reading.

with cpi_overall as (
    select date, cpi_index
    from {{ ref('stg_cpi') }}
    where division = 'overall'
),

joined as (
    select
        spine.date,
        cpi_overall.cpi_index
    from {{ ref('date_spine') }} as spine
    left join cpi_overall
        on spine.date = cpi_overall.date
),

grouped as (
    select
        *,
        count(cpi_index) over (order by date) as fill_group
    from joined
)

select
    date,
    first_value(cpi_index) over (partition by fill_group order by date) as cpi_index
from grouped
