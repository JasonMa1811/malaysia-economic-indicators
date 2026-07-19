-- OPR only changes a handful of times a year. Forward-fill onto every
-- day until the next rate change — same logic as before, just now
-- keyed by day instead of month to match the new daily grain.

with joined as (
    select
        spine.date,
        opr.new_opr_level
    from {{ ref('date_spine') }} as spine
    left join {{ ref('stg_opr') }} as opr
        on spine.date = opr.date
),

grouped as (
    select
        *,
        count(new_opr_level) over (order by date) as fill_group
    from joined
)

select
    date,
    first_value(new_opr_level) over (partition by fill_group order by date) as new_opr_level
from grouped
