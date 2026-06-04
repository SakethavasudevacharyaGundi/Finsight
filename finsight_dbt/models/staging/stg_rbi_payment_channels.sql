with source as (

    select *
    from {{ source(
        'raw',
        'RBI_PAYMENT_CHANNELS'
    ) }}

)

select

    cast(report_period as date)
        as report_period,

    metric_code,

    metric_name,

    cast(volume_lakh as number(18,5))
        as volume_lakh,

    cast(value_crore as number(18,5))
        as value_crore,

    md5(
        concat(
            report_period,
            metric_code
        )
    ) as channel_key,

    current_timestamp()
        as dbt_loaded_at

from source