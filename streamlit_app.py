import pandas as pd
import streamlit
import requests
import snowflake.connector

try:
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_cur = my_cnx.cursor()
    my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION();")
    my_data_row = my_cur.fetchone()
    my_cur.close()
    my_cnx.close()
except Exception as e:
    print(e)

streamlit.title('My Parents New Heathy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# NEW SECTION TO DISPLAY FRUITYVICE API RESPONSE
streamlit.header("Fruityvice Fruit Advice!")

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# streamlit.text(fruityvice_response.json())

# convert the json data to a CSV type format.
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())

# display normalized view
streamlit.dataframe(fruityvice_normalized)

conn = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = pd.read_sql("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION();", conn)

streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)
