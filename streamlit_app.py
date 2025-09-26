# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize Your smoothie")
st.write(
  """Choose fruits in your custom smoothie!
  """
)
# import streamlit as st

# option = st.selectbox(
#     "What is your favorite fruit?",
#     ("banana", "strawberries", "peaches"),
#     index=None,
# )

# st.write("You favorite fruit is:", option)


name_on_order = st.text_input("Name on smoothie:")
st.write("Name on your smoothie will be", name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect(
    'Choose upto 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
)

if ingredients_list:
    ingredients_string=''
    for fruit_choosen in ingredients_list:
        ingredients_string+=fruit_choosen+' '
        
    # st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    # st.write(my_insert_stmt)
    time_to_insert=st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")





        
