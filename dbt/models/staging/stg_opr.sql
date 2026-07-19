-- Mirrors etl/transform/transform.py::transform_opr()
-- Source occasionally has duplicate rows for the same date; keep one.
-- ctid (physical row location) approximates pandas' "keep first" since rows
-- land in the same order they were extracted from the API.

select distinct on (date)
    date::date as date,
    year,
    change_in_opr,
    new_opr_level
from {{ source('raw', 'opr') }}
order by date, ctid
