with source as (

    select *
    from {{ source('raw', 'UPI_MONTHLY_STATS') }}

),

cleaned as (

    select

        cast(month as date)
            as month,

        cast(banks_live as integer)
            as banks_live,

        cast(volume_mn as number(18,2))
            as volume_mn,

        cast(value_cr as number(18,2))
            as value_cr,

        source_file,

        md5(
            cast(month as varchar)
        ) as monthly_key,

        current_timestamp()
            as dbt_loaded_at

    from source

)

select *

from cleaned