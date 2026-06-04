with dates as (

    select distinct

        month

    from {{ ref('fact_upi_monthly') }}

)

select

    month as date_key,

    year(month) as year,

    quarter(month) as quarter,

    month(month) as month_number,

    monthname(month) as month_name,

    case
        when month(month) >= 4
        then concat(year(month), '-', year(month)+1)

        else concat(year(month)-1, '-', year(month))
    end as financial_year,

    case
        when date_trunc('month', current_date())
             =
             date_trunc('month', month)

        then true

        else false
    end as is_current_month

from dates