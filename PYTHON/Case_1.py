import pandas as pd
from sqlalchemy import create_engine


# Database connection
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


# Example usage
my_data = retrieve_data(
    product_code=18,
    store_code=1,
    date=['2019-01-01', '2019-01-31']
)

print(my_data.head())