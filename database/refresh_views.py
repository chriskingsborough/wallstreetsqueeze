 """Refresh views"""
from db_helpers import get_ps_conn, log_failure

def high_short():
    # -- high short interest
    # -- short percent outstanding > 10%
    # -- short percent float > 20%
    sql = """
    drop view if exists high_short cascade;
    create or replace view high_short as
    select
            s."ticker",
            s."shortName",
            s."price",
            s."marketCap",
            s."sector",
            s."industry",
            s."trailingAnnualDividendYield",
            s."forwardPE",
            s."forwardEps",
            s."fiftyTwoWeekLow",
            s."fiftyTwoWeekHigh",
            s."beta",
            s."shortPercentOutstanding",
            s."shortPercentOfFloat",
            s."calculatedShortPercentFloat",
            case
                when s."calculatedShortPercentFloat" is null
                    then s."shortPercentOfFloat"
                when s."shortPercentOfFloat" is null
                    then s."calculatedShortPercentFloat"
                when s."shortPercentOfFloat" < s."calculatedShortPercentFloat"
                    then s."shortPercentOfFloat"
                when s."shortPercentOfFloat" > s."calculatedShortPercentFloat"
                	then s."calculatedShortPercentFloat"
            end as "presShortPercentFloat"

    from (
        select
            si.ticker,
            si."shortName",
            sp.price,
            si."marketCap",
            si.sector,
            si.industry,
            si."trailingAnnualDividendYield",
            si."forwardPE",
            si."forwardEps",
            si."fiftyTwoWeekLow",
            si."fiftyTwoWeekHigh",
            si.beta,
            cast("sharesShort" as real)/cast("sharesOutstanding" as real) as "shortPercentOutstanding",
            "shortPercentOfFloat",
            cast("sharesShort" as real)/cast("floatShares" as real) as "calculatedShortPercentFloat"
        from stock_info si
        inner join stock_prices sp
            on si.ticker = sp.ticker
        where
            si."sharesShort" is not null
            and "sharesOutstanding" is not null
            and (cast("sharesShort" as real)/cast("sharesOutstanding" as real)) >= .10
            and coalesce(cast("sharesShort" as real)/cast("floatShares" as real), "shortPercentOfFloat") >= .20

    ) as s
    order by "presShortPercentFloat" desc
    ;
    """

    return sql

def dow_dogs():

    sql = """create or replace view dogs_of_the_dow as
    select
        si.ticker,
        si."shortName",
        sp.price,
        si."marketCap",
        si.sector,
        si.industry,
        si."trailingAnnualDividendYield",
        si."forwardPE",
        si.beta,
        case when sd.ticker is not null
            then 'Yes'
                else 'No'
        end "smallDog"
    from stock_info si
    inner join collections c
        on si.ticker = c.ticker
    inner join stock_prices sp
        on si.ticker = sp.ticker
    left join (
        -- small dogs of the dow
        select
            si.ticker
        from stock_info si
        inner join collections c
        on si.ticker = c.ticker
        where c.collection = 'Dow Jones'
            and si."trailingAnnualDividendYield" is not null
        order by "trailingAnnualDividendYield" desc
        limit 5
    ) as sd
    on si.ticker = sd.ticker
    where c.collection = 'Dow Jones'
        and si."trailingAnnualDividendYield" is not null
    order by "trailingAnnualDividendYield" desc
    limit 10;
    """

    return sql

def high_dividend():

    # -- High Dividend Yield
    # -- Need to add
    #     -- trailingAnnualDividendYield
    #     -- trailingAnnualDividendRate
    #     -- exDividendDate
    # -- check feasibility of exDividendDate within last year
    sql = """
    drop view if exists high_dividend;
    create or replace view high_dividend as
    select
        si.ticker,
        si."shortName",
        sp.price,
        si."marketCap",
        si.sector,
        si.industry,
        si."trailingAnnualDividendYield",
        si."trailingAnnualDividendRate",
        si."forwardPE",
        si.beta
    from stock_info si
    inner join stock_prices sp
        on si.ticker = sp.ticker
    where si."dividendYield" is not null
        and si."trailingAnnualDividendYield" is not null
        and si."exDividendDate" is not null
        and si."marketCap" > 500000000
    order by si."trailingAnnualDividendYield" desc
    ;"""

    return sql

def high_dividend_sans_reit():

    sql = """
    drop view if exists high_dividend_sans_reit;
    create or replace view high_dividend_sans_reit as
    select
        si.ticker,
        si."shortName",
        sp.price,
        si."marketCap",
        si.sector,
        si.industry,
        si."trailingAnnualDividendYield",
        si."trailingAnnualDividendRate",
        si."forwardPE",
        si.beta
    from stock_info si
    inner join stock_prices sp
        on si.ticker = sp.ticker
    where si."dividendYield" is not null
        and si."trailingAnnualDividendYield" is not null
        and si."exDividendDate" is not null
        and si.industry not like 'REIT%'
        and si."marketCap" > 500000000
    order by si."trailingAnnualDividendYield" desc
    ;"""

    return sql

def runners():

    sql = """
    drop view if exists runners;
    create or replace view runners as
    select
        si.ticker ,
        si."shortName" ,
        sp.price,
        si."fiftyDayAverage" ,
        si."twoHundredDayAverage",
        si."marketCap",
        si.sector,
        si.industry,
        si."trailingAnnualDividendYield",
        si."forwardPE",
        si.beta,
        si."fiftyTwoWeekLow",
        si."fiftyTwoWeekHigh",
        si."priceToSalesTrailing12Months"
    from stock_info si
    inner join stock_prices sp
        on si.ticker = sp.ticker
    where
        sp.price > si."fiftyDayAverage"
        and sp.price > si."twoHundredDayAverage"
        and si."fiftyDayAverage" > si."twoHundredDayAverage"
        and si."fiftyDayAverage" is not null
        and si."twoHundredDayAverage" is not null
    order by sp.price / si."fiftyDayAverage" desc
    limit 100;"""

    return sql

def dippers():

    sql = """
    drop view if exists dippers;
    create or replace view dippers as
    select
        si.ticker ,
        si."shortName" ,
        sp.price,
        si."fiftyDayAverage" ,
        si."twoHundredDayAverage",
        si."marketCap",
        si.sector,
        si.industry,
        si."trailingAnnualDividendYield",
        si."forwardPE",
        si.beta,
        si."fiftyTwoWeekLow",
        si."fiftyTwoWeekHigh",
        si."priceToSalesTrailing12Months"
    from stock_info si
    inner join stock_prices sp
        on si.ticker = sp.ticker
    where
        sp.price < si."fiftyDayAverage"
        and sp.price < si."twoHundredDayAverage"
        and si."fiftyDayAverage" is not null
        and si."twoHundredDayAverage" is not null
    order by sp.price / si."twoHundredDayAverage"
    limit 100;
    """

    return sql

def price_range_low():

    sql = """
    drop view if exists price_range_low;
    create or replace view price_range_low as
    select
        si.ticker,
        si."shortName",
        sp.price ,
        si."fiftyTwoWeekLow" ,
        si."fiftyTwoWeekHigh",
        (sp.price - si."fiftyTwoWeekLow")/(si."fiftyTwoWeekHigh" - si."fiftyTwoWeekLow") as "pricePercentOfRange",
        si."marketCap",
        si.sector,
        si.industry,
        si."trailingAnnualDividendYield",
        si."forwardPE",
        si.beta,
        si."fiftyDayAverage" ,
        si."twoHundredDayAverage",
        si."priceToSalesTrailing12Months"
    from stock_info si
    inner join stock_prices sp
        on si.ticker = sp.ticker
    where si."fiftyTwoWeekLow" is not null
        and si."fiftyTwoWeekHigh" is not null
        and (sp.price - si."fiftyTwoWeekLow")/(si."fiftyTwoWeekHigh" - si."fiftyTwoWeekLow") < .30
    order by (sp.price - si."fiftyTwoWeekLow")/(si."fiftyTwoWeekHigh" - si."fiftyTwoWeekLow") asc
    ;"""

    return sql

def price_range_high():

    sql = """
    drop view if exists price_range_high;
    create or replace view price_range_high as
    select
        si.ticker,
        si."shortName",
        sp.price ,
        si."fiftyTwoWeekLow" ,
        si."fiftyTwoWeekHigh",
        (sp.price - si."fiftyTwoWeekLow")/(si."fiftyTwoWeekHigh" - si."fiftyTwoWeekLow") as "pricePercentOfRange",
        si."marketCap",
        si.sector,
        si.industry,
        si."trailingAnnualDividendYield",
        si."forwardPE",
        si.beta,
        si."fiftyDayAverage" ,
        si."twoHundredDayAverage",
        si."priceToSalesTrailing12Months"
    from stock_info si
    inner join stock_prices sp
        on si.ticker = sp.ticker
    where si."fiftyTwoWeekLow" is not null
        and si."fiftyTwoWeekHigh" is not null
        and (sp.price - si."fiftyTwoWeekLow")/(si."fiftyTwoWeekHigh" - si."fiftyTwoWeekLow") > .70
    order by (sp.price - si."fiftyTwoWeekLow")/(si."fiftyTwoWeekHigh" - si."fiftyTwoWeekLow") desc
    ;
    """

    return sql

def pe_under_15():

    sql = """
    DROP VIEW IF EXISTS pe_under_fifteen;
    CREATE OR REPLACE VIEW pe_under_fifteen AS
    SELECT si.ticker,
        si."shortName",
        si."longName",
        sp.price,
        si."marketCap",
        si.sector,
        si.industry,
        si."trailingAnnualDividendYield",
        si."forwardPE",
        si."priceToBook",
        si."pegRatio",
        si."forwardEps",
        si.beta
    FROM stock_info si
         JOIN stock_prices sp ON si.ticker::text = sp.ticker::text
    where si."forwardPE" between 0 and 15
    	and si."forwardPE" is not null
    order by "marketCap" desc
    limit 100
    """

    return sql

def pb_under_one():

    sql = """
    DROP VIEW IF EXISTS pb_under_one;
    CREATE OR REPLACE VIEW pb_under_one AS
    SELECT si.ticker,
        si."shortName",
        si."longName",
        sp.price,
        si."marketCap",
        si.sector,
        si.industry,
        si."trailingAnnualDividendYield",
        si."forwardPE",
        si."priceToBook",
        si."pegRatio",
        si."forwardEps",
        si.beta
    FROM stock_info si
         JOIN stock_prices sp ON si.ticker::text = sp.ticker::text
    where si."priceToBook" between 0.01 and 1.0
    	and si."priceToBook" is not null
    order by si."marketCap" desc
    limit 100
    ;
    """

    return sql

def peg_under_one():

    sql = """
    DROP VIEW IF EXISTS peg_under_one;
    CREATE OR REPLACE VIEW peg_under_one AS
    SELECT si.ticker,
        si."shortName",
        si."longName",
        sp.price,
        si."marketCap",
        si.sector,
        si.industry,
        si."trailingAnnualDividendYield",
        si."forwardPE",
        si."priceToBook",
        si."pegRatio",
        si."forwardEps",
        si.beta
       FROM stock_info si
         JOIN stock_prices sp ON si.ticker::text = sp.ticker::text
    where si."pegRatio" between 0.01 and 1.0
    	and si."pegRatio" is not null
    order by "marketCap" desc
    limit 100
    ;
    """

    return sql

def stock_basics():

    sql = """
    DROP VIEW IF EXISTS stock_basics;
    CREATE OR REPLACE VIEW stock_basics AS
    SELECT si.ticker,
        si."shortName",
        si."longName",
        si."longBusinessSummary",
        si."logo_url",
        si.sector,
        si.industry,
        si.state,
        si.country ,
        si.website ,
        sp.price,
        si."fiftyTwoWeekLow",
        si."fiftyTwoWeekHigh",
        si."fiftyDayAverage",
        si."twoHundredDayAverage",
        si."marketCap",
        si."trailingAnnualDividendYield",
        si."trailingAnnualDividendRate",
        si."floatShares" ,
        si."sharesOutstanding" ,
        si."lastDividendDate" ,
        si."lastDividendValue" ,
        si."exDividendDate",
        si."trailingPE",
        si."forwardPE",
        si."priceToBook",
        si."pegRatio",
        si."trailingEps",
        si."forwardEps",
        si.beta,
        COALESCE(hs."presShortPercentFloat", si."shortPercentOfFloat", 0) as "shortPercentOfFloat",
        si."sharesShort",
        si."sharesShortPriorMonth",
        si."priceToSalesTrailing12Months",
        si."profitMargins",
        si."earningsQuarterlyGrowth"
    FROM stock_info si
    JOIN stock_prices sp ON si.ticker::text = sp.ticker::text
    LEFT JOIN
        high_short hs ON si.ticker::text = hs.ticker::text
    ;
    """

    return sql

def _others():

    """-- Price to book ratio under 1
    select
        si.ticker ,
        si."shortName" ,
        si.industry ,
        si."priceToBook"
    from stock_info si
    where si."priceToBook" is not null
        and si."priceToBook" < 1
    order by si."priceToBook" desc;

    -- PE Ratio
    select
        si.ticker ,
        si."shortName" ,
        si.industry ,
        si."priceToBook"
    from stock_info si
    where si."priceToBook" is not null
    order by si."priceToBook" desc
    ;

    -- penny stocks
    select
        sp.price ,
        si.*
    from stock_info si
    inner join stock_prices sp
        on si.ticker = sp.ticker
    where
        sp.price < 5.00
        and sp.price is not null
        and si."marketCap" < 5000000000
        and si."marketCap" is not null
    ;

    -- beta
    select
        beta,
        si.*
    from stock_info si
    where beta is not null
    order by beta desc
    limit 50;
    """

def create_view(sql):

    try:
        conn = get_ps_conn()
        cur = conn.cursor()

        cur.execute(sql)
        conn.commit()
    except Exception as e:
        print(sql)
        print(e)
    finally:
        conn.close()


if __name__ == '__main__':

    # high short
    create_view(high_short())
    create_view(dow_dogs())
    create_view(high_dividend())
    create_view(high_dividend_sans_reit())
    create_view(runners())
    create_view(dippers())
    create_view(price_range_low())
    create_view(price_range_high())
    create_view(pe_under_15())
    create_view(pb_under_one())
    create_view(peg_under_one())
    create_view(stock_basics())
