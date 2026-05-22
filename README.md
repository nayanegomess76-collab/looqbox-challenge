# looqbox-challenge


#Question 1

##Objective
Retrieve the 10 most expensive products in the company.

##SQL Query

```sql
SELECT
    PRODUCT_COD,
    PRODUCT_NAME,
    PRODUCT_VAL
FROM data_product
ORDER BY PRODUCT_VAL DESC
LIMIT 10;
```

##Explanation
The query orders the products by value in descending order and returns only the top 10 most expensive products.

##Result
Screenshot saved in:
images/question1_SQL_result.png




#Question 2

##Objective
Retrieve all sections that belong to the 'BEBIDAS' and 'PADARIA' departments.

##SQL Query

```sql
SELECT DISTINCT
    DEP_NAME,
    SECTION_NAME
FROM data_product
WHERE DEP_NAME IN ('BEBIDAS', 'PADARIA');
```

##Explanation
The query filters the departments 'BEBIDAS' and 'PADARIA' and returns their distinct sections without duplicates.

##Result
Screenshot saved in:
images/question2_SQL_result.png




#Question 3

##Objective
Calculate the total sales value of products for each business area during the first quarter of 2019.

##SQL query
``` sql
SELECT
    c.BUSINESS_NAME,
    SUM(s.SALES_VALUE) AS TOTAL_SALES
FROM data_product_sales s
JOIN data_store_cad c
    ON s.STORE_CODE = c.STORE_CODE
WHERE s.DATE BETWEEN '2019-01-01' AND '2019-03-31'
GROUP BY c.BUSINESS_NAME
ORDER BY TOTAL_SALES DESC;
```

##Explanation
The query joins the sales and store tables using STORE_CODE, filters the first quarter of 2019,
and calculates the total sales value for each business area.

##Result
Screenshot saved in:
images/question3_SQL_result.png


----------------------------------------------------------------------------

##Python Cases

#Case 1

##Objective
Create a dynamic Python function capable of retrieving sales data based on optional filters such as product code,
 store code, and date range.

##Python Code

import pandas as pd
from sqlalchemy import create_engine


#Database connection
engine = create_engine(
    "mysql+pymysql://looqbox-challenge:looq-challenge@35.199.115.174:3306/looqbox-challenge"
)


def retrieve_data(product_code=None, store_code=None, date=None):

    # Base query
    query = """
    SELECT *
    FROM data_product_sales
    WHERE 1=1
    """

    # Adds product filter
    if product_code:
        query += f" AND PRODUCT_CODE = {product_code}"

    # Adds store filter
    if store_code:
        query += f" AND STORE_CODE = {store_code}"

    # Adds date filter
    if date:
        query += f" AND DATE BETWEEN '{date[0]}' AND '{date[1]}'"

    # Executes query and stores dataframe
    df = pd.read_sql(query, engine)

    return df


#Example usage
my_data = retrieve_data(
    product_code=18,
    store_code=1,
    date=['2019-01-01', '2019-01-31']
)

print(my_data.head())


##Explanation
The function dynamically builds a SQL query according to the parameters provided by the user 
and returns the result as a pandas dataframe.

##Result
Screenshot saved in:
images/case1_PY_output.png


-----------------------------------------------------------------------------------------------------

#Case 2

##Objective
Use the two provided queries without modifying them, apply the requested date filter, and recreate the requested visualization using Python.

##Python Code

```python
# import pandas as pd
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
```

##Explanation
The solution reads the two provided queries into pandas dataframes, applies the requested date filter between 2019-10-01 and 2019-12-31, merges the tables using STORE_CODE, and calculates the TM (Average Ticket) metric by dividing SALES_VALUE by SALES_QTY. The final table groups the results by store and business category.

##Result
Result displayed in terminal and exported to:
images/case2_table.csv
images/case2_PY_table.png




-----------------------------------------------------------------------------------------

#Case 3

##Objective
Create a custom visualization using data from the IMDB_movies table and explain the reasoning behind the chosen chart.

##Python Code

```python
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Database connection
engine = create_engine(
    "mysql+pymysql://looqbox-challenge:looq-challenge@35.199.115.174:3306/looqbox-challenge"
)

# Query
query = """
SELECT
    Genre,
    Rating
FROM IMDB_movies
"""

# Reads data
df = pd.read_sql(query, engine)

# Removes null values
df = df.dropna()

# Splits genres separated by commas
df['Genre'] = df['Genre'].str.split(',')

# Explodes genres into multiple rows
df = df.explode('Genre')

# Removes extra spaces
df['Genre'] = df['Genre'].str.strip()

# Calculates average rating by genre
genre_rating = (
    df.groupby('Genre')['Rating']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

# Creates chart
ax = genre_rating.plot(
    kind='bar',
    figsize=(10, 6)
)

# Chart labels
plt.title('Top 10 Genres by Average IMDb Rating')
plt.xlabel('Genre')
plt.ylabel('Average Rating')

# Rotates labels
plt.xticks(rotation=45)

# Adds values above bars
for p in ax.patches:
    ax.annotate(
        f"{p.get_height():.1f}",
        (p.get_x() + p.get_width() / 2, p.get_height()),
        ha='center',
        va='bottom'
    )

# Adjusts layout
plt.tight_layout()

# Saves chart
plt.savefig('images/case3_chart.png')

# Displays chart
plt.show()
```

##Explanation
The solution reads movie genres and ratings from the IMDB_movies table, cleans the data, separates movies with multiple genres,
 and calculates the average IMDb rating for each genre. A bar chart was chosen because it provides a clear comparison between categories 
 and makes it easy to identify the highest-rated genres.

## Result
Screenshot saved in:
images/case3_PY_result.png