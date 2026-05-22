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