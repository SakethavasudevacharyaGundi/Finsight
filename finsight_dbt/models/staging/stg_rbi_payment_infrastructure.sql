with source as (

    select *
    from {{ source(
        'raw',
        'RBI_PAYMENT_INFRASTRUCTURE'
    ) }}

)

select

    report_period,

    metric_code,

    metric_name,

    cast(metric_value as number(18,5))
        as metric_value,

    md5(
        concat(
            report_period,
            metric_code
        )
    ) as infrastructure_key,

    current_timestamp()
        as dbt_loaded_at

from source