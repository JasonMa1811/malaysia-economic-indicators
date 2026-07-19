-- Mirrors etl/transform/transform.py::transform_fuelprice()
-- Keep only the 'level' series (as opposed to week-over-week % change rows),
-- and drop the now-redundant series_type flag.

select
    date::date as date,
    ron95,
    ron97,
    diesel,
    ron95_skps,
    diesel_budi,
    diesel_skds,
    ron95_budi95,
    diesel_eastmsia
from {{ source('raw', 'fuelprice') }}
where series_type = 'level'
