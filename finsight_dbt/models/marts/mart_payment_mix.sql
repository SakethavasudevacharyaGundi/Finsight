with transactions as (

    select *

    from {{ ref('stg_rbi_payment_transactions') }}

    where metric_name in (

        'UPI @',
        'NEFT',
        'IMPS',
        'Credit Transfers - RTGS',
        'Credit Cards',
        'Debit Cards',
        'Wallets',
        'AePS (Fund Transfers) @'

    )

),

totals as (

    select

        report_period,

        sum(volume_lakh) as total_volume,

        sum(value_crore) as total_value

    from transactions

    group by report_period

)

select

    t.report_period,

    t.metric_name as payment_channel,

    t.volume_lakh,

    t.value_crore,

    round(
        t.volume_lakh
        / nullif(x.total_volume, 0)
        * 100,
        2
    ) as volume_share_pct,

    round(
        t.value_crore
        / nullif(x.total_value, 0)
        * 100,
        2
    ) as value_share_pct,

    rank() over (
        partition by t.report_period
        order by t.volume_lakh desc
    ) as volume_rank,

    rank() over (
        partition by t.report_period
        order by t.value_crore desc
    ) as value_rank,

    current_timestamp() as mart_loaded_at

from transactions t

join totals x

    on t.report_period = x.report_period