with source as (

    select *
    from {{ ref('stg_upi_monthly') }}

)

select

    month,

    banks_live,

    volume_mn,

    value_cr,

    round(
        value_cr / nullif(volume_mn, 0),
        2
    ) as avg_ticket_size,

    current_timestamp() as created_at

from source