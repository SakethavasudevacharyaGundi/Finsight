with source as (

    select *
    from {{ source(
        'raw',
        'RBI_PAYMENT_FRAUDS'
    ) }}

)

select

    cast(report_period as date)
        as report_period,

    cast(fraud_volume_lakh as number(18,5))
        as fraud_volume_lakh,

    cast(fraud_value_crore as number(18,5))
        as fraud_value_crore,

    current_timestamp()
        as dbt_loaded_at

from source