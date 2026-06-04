with source as (

    select *
    from {{ source('raw', 'UPI_DAILY_STATS') }}

),

cleaned as (

    select

        cast(report_date as date) as report_date,

        cast(volume_mn as number(18,2))
            as volume_mn,

        cast(value_cr as number(18,2))
            as value_cr,

        current_timestamp()
            as dbt_loaded_at

    from source

)

select *

from cleaned