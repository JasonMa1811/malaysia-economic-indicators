-- Mirrors etl/transform/transform.py::transform_cpi() and its division_map dict.
-- Maps DOSM's COICOP division codes to human-readable category names.

select
    date::date as date,
    index as cpi_index,
    division,
    case division
        when 'overall' then 'Overall'
        when '01' then 'Food & Non-Alcoholic Beverages'
        when '02' then 'Alcoholic Beverages & Tobacco'
        when '03' then 'Clothing & Footwear'
        when '04' then 'Housing, Water, Electricity & Gas'
        when '05' then 'Furnishings & Household Equipment'
        when '06' then 'Health'
        when '07' then 'Transport'
        when '08' then 'Communication'
        when '09' then 'Recreation & Culture'
        when '10' then 'Education'
        when '11' then 'Restaurants & Hotels'
        when '12' then 'Miscellaneous Goods & Services'
        when '13' then 'Insurance & Financial Services'
    end as division_name
from {{ source('raw', 'cpi') }}
