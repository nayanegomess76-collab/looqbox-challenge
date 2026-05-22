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

# Calculates Ticket Average (TM)
df_merged['TM'] = (
    df_merged['SALES_VALUE'] /
    df_merged['SALES_QTY']
)

# Groups by store and business category
tm_table = (
    df_merged.groupby(
        ['STORE_NAME', 'BUSINESS_NAME']
    )['TM']
    .mean()
    .reset_index()
)

# Renames columns
tm_table.columns = ['Store', 'Category', 'TM']

# Rounds values
tm_table['TM'] = tm_table['TM'].round(2)

# Displays result
print(tm_table.head(20))

# Saves table
tm_table.to_csv(
    'images/case2_table.csv',
    index=False
)
# Creates table figure
fig, ax = plt.subplots(figsize=(10, 6))

# Removes axes
ax.axis('off')

# Creates table
table = ax.table(
    cellText=tm_table.values,
    colLabels=tm_table.columns,
    loc='center'
)

# Adjusts style
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.5)

# Saves image
plt.savefig(
    'images/case2_table.png',
    bbox_inches='tight'
)

# Displays image
plt.show()
