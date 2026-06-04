with upi as (

    select *

    from {{ ref('fact_upi_monthly') }}

)

select

    month,

    banks_live,

    volume_mn,

    value_cr,

    avg_ticket_size,

    --------------------------------------------------
    -- Previous Month
    --------------------------------------------------

    lag(volume_mn) over (
        order by month
    ) as prev_volume_mn,

    lag(value_cr) over (
        order by month
    ) as prev_value_cr,

    lag(banks_live) over (
        order by month
    ) as prev_banks_live,

    lag(avg_ticket_size) over (
        order by month
    ) as prev_avg_ticket_size,

    --------------------------------------------------
    -- MoM Growth
    --------------------------------------------------

    round(

        (
            volume_mn
            -
            lag(volume_mn) over (
                order by month
            )
        )

        /

        nullif(
            lag(volume_mn) over (
                order by month
            ),
            0
        )

        * 100,

        2

    ) as volume_growth_mom_pct,

    round(

        (
            value_cr
            -
            lag(value_cr) over (
                order by month
            )
        )

        /

        nullif(
            lag(value_cr) over (
                order by month
            ),
            0
        )

        * 100,

        2

    ) as value_growth_mom_pct,

    round(

        (
            banks_live
            -
            lag(banks_live) over (
                order by month
            )
        )

        /

        nullif(
            lag(banks_live) over (
                order by month
            ),
            0
        )

        * 100,

        2

    ) as bank_growth_mom_pct,

    round(

        (
            avg_ticket_size
            -
            lag(avg_ticket_size) over (
                order by month
            )
        )

        /

        nullif(
            lag(avg_ticket_size) over (
                order by month
            ),
            0
        )

        * 100,

        2

    ) as ticket_size_growth_mom_pct,

    --------------------------------------------------
    -- YoY Growth
    --------------------------------------------------

    round(

        (
            volume_mn
            -
            lag(volume_mn, 12) over (
                order by month
            )
        )

        /

        nullif(
            lag(volume_mn, 12) over (
                order by month
            ),
            0
        )

        * 100,

        2

    ) as volume_growth_yoy_pct,

    round(

        (
            value_cr
            -
            lag(value_cr, 12) over (
                order by month
            )
        )

        /

        nullif(
            lag(value_cr, 12) over (
                order by month
            ),
            0
        )

        * 100,

        2

    ) as value_growth_yoy_pct,

    current_timestamp() as mart_loaded_at

from upi