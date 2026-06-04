with source as (

    select *
    from {{ source(
        'raw',
        'RBI_DPI'
    ) }}

)

select

    cast(period as date)
        as period,

    cast(dpi_value as number(18,2))
        as dpi_value,

    current_timestamp()
        as dbt_loaded_at

from source