with dpi as (

    select

        period,
        dpi_value

    from {{ ref('stg_rbi_dpi') }}

),

upi as (

    select

        month,
        banks_live,
        volume_mn,
        value_cr,
        avg_ticket_size

    from {{ ref('fact_upi_monthly') }}

)

select

    d.period,

    d.dpi_value,

    u.banks_live,

    u.volume_mn as upi_volume_mn,

    u.value_cr as upi_value_cr,

    u.avg_ticket_size,

    round(

        (
            d.dpi_value
            -
            lag(d.dpi_value) over (
                order by d.period
            )
        )

        /

        nullif(
            lag(d.dpi_value) over (
                order by d.period
            ),
            0
        )

        * 100,

        2

    ) as dpi_growth_pct,

    current_timestamp() as mart_loaded_at

from dpi d

left join upi u

    on d.period = u.month