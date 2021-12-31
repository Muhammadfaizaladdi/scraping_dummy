import extract 
import transform
import load
import pandas as pd

# Extract the content
url = "https://webscraper.io/test-sites/e-commerce/static/computers/tablets?page="
pages = 4
parser_type = "html.parser"

parsed_content = extract.extract_html_content(url, pages, parser_type)

# get elemen (title, price, description, number of review)
# get title
tag = 'a'
class_el = 'title'
titles = extract.get_elemen(tag, parsed_content, class_el)

# get price
tag = 'h4'
class_el = 'price'
price = extract.get_elemen(tag, parsed_content, class_el)

# get description
tag = 'p'
class_el = 'description'
desc = extract.get_elemen(tag, parsed_content, class_el)

# get number of review
tag = 'p'
class_el = 'pull-right'
num_of_review = extract.get_elemen(tag, parsed_content, class_el)

# Create Data Frame
df = pd.DataFrame({
    'title' : titles,
    'price' : price,
    'description' : desc,
    'num_of_review' : num_of_review
})

# Transformation (construct id, convert price to decimal, convert review to integer)
# clean price column
df['price'] = df['price'].str.replace("$", "")

# create id
df['id'] = transform.construct_id(df, 'title', 'price')

# convert to decimal
df['price'] = pd.to_numeric(df['price'])

# convert number of review
df['num_of_review'] = df['num_of_review'].apply(lambda rev: rev.split()[0]).astype('int64')


# load
# create connection object (connect to db)
host_name = 'localhost'
user_name = 'root'
password = 'hmmm_mantap'
db = 'crawl_web'

connection = load.create_db_connection(host_name, user_name, password, db)

# create table
query = """
  CREATE TABLE IF NOT EXISTS tugas_faizal (
    id VARCHAR(255) PRIMARY KEY NOT NULL,
    title VARCHAR(255),
    price DECIMAL(10,2),
    description TEXT,
    num_of_review INT
  )
"""

load.execute_query(connection, query)

# Insert Data
# Create list of record
list_tab_dict = []

for i in range(len(df)):
    temp_dict = {}
    temp_dict["id_column"] = df.loc[i:i, 'id'].tolist()[0]
    temp_dict["title_column"] = df.loc[i:i, 'title'].tolist()[0]
    temp_dict["price_column"] = df.loc[i:i, 'price'].tolist()[0]
    temp_dict["description"] = df.loc[i:i, 'description'].tolist()[0]
    temp_dict["num_of_review"] = df.loc[i:i, 'num_of_review'].tolist()[0]
    
    list_tab_dict.append(temp_dict)

query = """
  INSERT INTO digitalskola.tugas_faizal (id, title, price, description, num_of_review)
  VALUES (%s, %s, %s, %s, %s)
"""

for tab in list_tab_dict:
  data = (tab["id_column"], tab["title_column"], tab["price_column"], 
          tab["description"], tab["num_of_review"])
  load.execute_query(query, data)