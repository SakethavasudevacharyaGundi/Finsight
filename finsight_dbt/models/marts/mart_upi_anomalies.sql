with upi as (

    select *

    from {{ ref('fact_upi_monthly') }}

),

stats as (

    select

        month,

        volume_mn,

        value_cr,

        avg_ticket_size,

        avg(volume_mn) over (

            order by month

            rows between 5 preceding
            and current row

        ) as rolling_avg_6m,

        stddev(volume_mn) over (

            order by month

            rows between 5 preceding
            and current row

        ) as rolling_std_6m

    from upi

)

select

    month,

    volume_mn,

    value_cr,

    avg_ticket_size,

    rolling_avg_6m,

    rolling_std_6m,

    round(

        (
            volume_mn
            -
            rolling_avg_6m
        )

        /

        nullif(
            rolling_std_6m,
            0
        ),

        2

    ) as z_score,

    case

        when abs(

            (
                volume_mn
                -
                rolling_avg_6m
            )

            /

            nullif(
                rolling_std_6m,
                0
            )

        ) > 2

        then true

        else false

    end as is_anomaly,

    current_timestamp() as mart_loaded_at

from stats