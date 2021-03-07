"""empty message

Revision ID: 94f92e43632b
Revises: 01cc7c443cb1
Create Date: 2021-03-01 19:59:43.982865

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '94f92e43632b'
down_revision = '01cc7c443cb1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('collection_changes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ticker', sa.String(), nullable=True),
    sa.Column('collection', sa.String(), nullable=True),
    sa.Column('change', sa.String(), nullable=True),
    sa.Column('data', sa.DATE(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('collections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ticker', sa.String(), nullable=True),
    sa.Column('collection', sa.String(), nullable=True),
    sa.Column('last_updated', sa.DATE(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('index_prices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ticker', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('date', sa.DATE(), nullable=True),
    sa.Column('previous_close', sa.REAL(), nullable=True),
    sa.Column('close', sa.REAL(), nullable=True),
    sa.Column('dollar_change', sa.REAL(), nullable=True),
    sa.Column('decimal_change', sa.REAL(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stock_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ticker', sa.String(), nullable=True),
    sa.Column('shortName', sa.String(), nullable=True),
    sa.Column('longName', sa.String(), nullable=True),
    sa.Column('sector', sa.String(), nullable=True),
    sa.Column('industry', sa.String(), nullable=True),
    sa.Column('longBusinessSummary', sa.String(), nullable=True),
    sa.Column('state', sa.String(), nullable=True),
    sa.Column('country', sa.String(), nullable=True),
    sa.Column('website', sa.String(), nullable=True),
    sa.Column('logo_url', sa.String(), nullable=True),
    sa.Column('marketCap', sa.Integer(), nullable=True),
    sa.Column('beta', sa.REAL(), nullable=True),
    sa.Column('enterpriseValue', sa.REAL(), nullable=True),
    sa.Column('netIncomeToCommon', sa.Integer(), nullable=True),
    sa.Column('fiftyTwoWeekLow', sa.REAL(), nullable=True),
    sa.Column('fiftyTwoWeekHigh', sa.REAL(), nullable=True),
    sa.Column('fiftyTwoWeekChange', sa.REAL(), nullable=True),
    sa.Column('fiftyDayAverage', sa.REAL(), nullable=True),
    sa.Column('dividendRate', sa.REAL(), nullable=True),
    sa.Column('dividendYield', sa.REAL(), nullable=True),
    sa.Column('lastDividendDate', sa.DATE(), nullable=True),
    sa.Column('lastDividendValue', sa.REAL(), nullable=True),
    sa.Column('floatShares', sa.Integer(), nullable=True),
    sa.Column('sharesOutstanding', sa.Integer(), nullable=True),
    sa.Column('sharesShort', sa.Integer(), nullable=True),
    sa.Column('sharesShortPriorMonth', sa.Integer(), nullable=True),
    sa.Column('shortPercentOfFloat', sa.REAL(), nullable=True),
    sa.Column('shortRatio', sa.REAL(), nullable=True),
    sa.Column('trailingPE', sa.REAL(), nullable=True),
    sa.Column('forwardPE', sa.REAL(), nullable=True),
    sa.Column('trailingEps', sa.REAL(), nullable=True),
    sa.Column('forwardEps', sa.REAL(), nullable=True),
    sa.Column('bookValue', sa.REAL(), nullable=True),
    sa.Column('enterpriseToEbitda', sa.REAL(), nullable=True),
    sa.Column('enterpriseToRevenue', sa.REAL(), nullable=True),
    sa.Column('payoutRatio', sa.REAL(), nullable=True),
    sa.Column('priceToSalesTrailing12Months', sa.REAL(), nullable=True),
    sa.Column('profitMargins', sa.REAL(), nullable=True),
    sa.Column('priceToBook', sa.REAL(), nullable=True),
    sa.Column('pegRatio', sa.REAL(), nullable=True),
    sa.Column('earningsQuarterlyGrowth', sa.REAL(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stock_prices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ticker', sa.String(), nullable=True),
    sa.Column('last_updated', sa.DATE(), nullable=True),
    sa.Column('price', sa.REAL(), nullable=True),
    sa.Column('volume', sa.REAL(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('stocks')
    op.drop_table('indices')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('indices',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('ticker', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('previous_close', sa.REAL(), autoincrement=False, nullable=True),
    sa.Column('close', sa.REAL(), autoincrement=False, nullable=True),
    sa.Column('dollar_change', sa.REAL(), autoincrement=False, nullable=True),
    sa.Column('decimal_change', sa.REAL(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='indices_pkey')
    )
    op.create_table('stocks',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('ticker', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('collection', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('info', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='stocks_pkey')
    )
    op.drop_table('stock_prices')
    op.drop_table('stock_info')
    op.drop_table('index_prices')
    op.drop_table('collections')
    op.drop_table('collection_changes')
    # ### end Alembic commands ###
