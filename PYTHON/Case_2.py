import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Database connection
engine = create_engine(
    "mysql+pymysql://looqbox-challenge:looq-challenge@35.199.115.174:3306/looqbox-challenge"
)

# Query 1
query_1 = """
SELECT
    STORE_CODE,
    STORE_NAME,
    START_DATE,
    END_DATE,
    BUSINESS_NAME,
    BUSINESS_CODE
FROM data_store_cad
"""

# Query 2
query_2 = """
SELECT
    STORE_CODE,
    DATE,
    SALES_VALUE,
    SALES_QTY
FROM data_store_sales
WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
"""

# Reads queries into dataframes
df_store = pd.read_sql(query_1, engine)
df_sales = pd.read_sql(query_2, engine)

# Converts DATE column to datetime
df_sales['DATE'] = pd.to_datetime(df_sales['DATE'])

# Additional filter requested by the challenge
df_sales = df_sales[
    (df_sales['DATE'] >= '2019-10-01') &
    (df_sales['DATE'] <= '2019-12-31')
]

# Merge dataframes
df_merged = pd.merge(
    df_sales,
    df_store,
    on='STORE_CODE',
    how='inner'
)

# Groups total sales by business area
sales_by_business = df_merged.groupby(
    'BUSINESS_NAME'
)['SALES_VALUE'].sum().sort_values(ascending=False)

# Creates chart
ax = sales_by_business.plot(
    kind='bar',
    figsize=(10, 6)
)

# Chart labels
plt.title('Total Sales by Business Area')
plt.xlabel('Business Area')
plt.ylabel('Total Sales Value')

# Rotates labels
plt.xticks(rotation=45)

# Adds values above bars
for p in ax.patches:
    ax.annotate(
        f"{p.get_height():,.0f}",
        (p.get_x() + p.get_width() / 2, p.get_height()),
        ha='center',
        va='bottom'
    )

# Adjusts layout
plt.tight_layout()

# Saves image
plt.savefig('images/case2_chart.png')

# Displays chart
plt.show()