with frauds as (

    select *

    from {{ ref('stg_rbi_payment_frauds') }}

)

select

    report_period,

    fraud_volume_lakh,

    fraud_value_crore,

    lag(fraud_volume_lakh) over (
        order by report_period
    ) as prev_fraud_volume,

    lag(fraud_value_crore) over (
        order by report_period
    ) as prev_fraud_value,

    round(
        (
            fraud_volume_lakh
            - lag(fraud_volume_lakh) over (
                order by report_period
            )
        )
        /
        nullif(
            lag(fraud_volume_lakh) over (
                order by report_period
            ),
            0
        )
        * 100,
        2
    ) as fraud_volume_growth_pct,

    round(
        (
            fraud_value_crore
            - lag(fraud_value_crore) over (
                order by report_period
            )
        )
        /
        nullif(
            lag(fraud_value_crore) over (
                order by report_period
            ),
            0
        )
        * 100,
        2
    ) as fraud_value_growth_pct,

    round(
        avg(fraud_volume_lakh) over (
            order by report_period
            rows between 2 preceding and current row
        ),
        2
    ) as rolling_3m_volume_avg,

    round(
        avg(fraud_value_crore) over (
            order by report_period
            rows between 2 preceding and current row
        ),
        2
    ) as rolling_3m_value_avg,

    current_timestamp() as mart_loaded_at

from frauds