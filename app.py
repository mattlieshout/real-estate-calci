import streamlit as st
import pandas as pd
import altair as alt
import shap
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.ensemble import RandomForestRegressor
from requests import get
from bs4 import BeautifulSoup
from functions import *
from calc_display import *


# def price_mine(url):
#     # Currently this function takes an input of a URL and returns the listing prices
#     response = get(url)
#     response_text = response.text
#     html_soup = BeautifulSoup(response_text, 'html.parser')
#     prices = html_soup.find(class_="bVPpjr")
#     return prices

avatar1 = "https://www.w3schools.com/howto/img_avatar1.png"
avatar2 = "https://www.w3schools.com/howto/img_avatar2.png"

title_temp = """
	<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
	<h4 style="color:white;text-align:center;">{}</h1>
	<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
	<h6>Author:{}</h6>
	<br/>
	<br/>	
	<p style="text-align:justify">{}</p>
	</div>
	"""
article_temp = """
	<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
	<h4 style="color:white;text-align:center;">{}</h1>
	<h6>Author:{}</h6> 
	<h6>Post Date: {}</h6>
	<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;width: 50px;height: 50px;" >
	<br/>
	<br/>
	<p style="text-align:justify">{}</p>
	</div>
	"""
head_message_temp = """
	<div style="background-color:white;padding:10px;border-radius:5px;margin:10px;border-style: solid;border-color: gray;">
	<h4 style="color:gray;text-align:Left;">Address: {}</h1>
	<img src="{}" alt="Avatar" style="vertical-align: center;float:right;max-height: 100px"; padding:10px>
	<h6>Purchase Price: ${}</h6> 	
	<h6>Number of Units: {}</h6>
	<h6>Cash on Cash Return: {}%</h6>	
	</div>
	"""
full_message_temp = """
	<div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
		<p style="text-align:justify;color:black;padding:10px">{}</p>
	</div>
	"""

HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""
init_url = "https://www.realtor.com/"
init_propery_image = "https://dr5dymrsxhdzh.cloudfront.net/blog/images/afe7b83e7/2018/10/calculator.jpg"
init_property_address = "Enter Address"
init_purch_price = 800000
init_rehab_costs = 0
init_rental_income = 4000
init_units = 2
init_rental_growth = 2.0
init_capital_gain = 2.0
init_downpayment = 5.0
init_loan_length = 30
init_interest_rate = 3.0
init_insurance = 2000
init_prop_tax = 10000
init_capex = 5
init_vacancy = 5
init_repairs_maintain = 5
init_management_fee = 8
init_expense_growth = 2.0
init_rehab_costs = "0"

menu = ["Home", "Add New Property", "Saved Properties", "Edit Properties", "Delete Properties"]

choice = st.sidebar.selectbox("Menu", menu)
# create_table()
if choice == "Home":
    st.header("Welcome Back!")
    st.subheader("Prior Properties")
    result = view_all_notes()
    for i in result:
        short_article = str(i[2])[0:50]
        st.write(head_message_temp.format(i[2], i[1], i[3], i[5], i[18], i[19]), unsafe_allow_html=True)

elif choice == "Add New Property":
    property_info = [init_property_address,init_url,init_propery_image,init_purch_price,init_rehab_costs, init_rental_income,init_units,init_rental_growth,init_capital_gain,init_downpayment,init_loan_length,init_interest_rate,
                    init_insurance,init_prop_tax,init_capex,init_vacancy,init_repairs_maintain,init_management_fee,init_expense_growth, init_rehab_costs]
    new_prop = calculate_results(property_info, False)
    # if st.button("Save New Property"):
    #     add_data(new_prop)
    #     st.success("{} saved".format(new_prop[0]))


elif choice == "Saved Properties":
    st.subheader("Saved Properties")
    all_titles = [i[0] for i in view_all_titles()]
    postlist = st.sidebar.selectbox("Posts", all_titles)
    post_result = get_blog_by_property_address(postlist)
    # st.write(post_result)
    for i in post_result:
        st.markdown(head_message_temp.format(i[2], i[1], i[3], i[5], round(float(i[19]),2)), unsafe_allow_html=True)
        # st.markdown(full_message_temp.format(i[2]), unsafe_allow_html=True)

# elif choice == "Search":
#     st.subheader("Search")
#     st.subheader("Search Properties")
#     search_term = st.text_input("Enter Term")
#     search_choice = "Address"
#     if st.button('Search'):
#         if search_choice == "Address":
#             article_result = get_blog_by_property_address(search_term)
#         # elif search_choice == "author":
#         #     article_result = get_blog_by_author(search_term)
#
#         # Preview Articles
#         for i in article_result:
#             # st.text("Reading Time:{} minutes".format(readingTime(str(i[2]))))
#             # st.write(article_temp.format(i[1],i[0],i[3],i[2]),unsafe_allow_html=True)
#             st.write(head_message_temp.format(i[2], i[1], i[3], i[5], i[18], i[19]), unsafe_allow_html=True)
#             st.write(full_message_temp.format(i[2]), unsafe_allow_html=True)

elif choice == "Delete Properties":
    st.subheader("Delete Properties")
    result = view_all_notes()

    # clean_db = pd.DataFrame(result,
    #                         columns=['property_address', 'url', 'propery_image', 'purch_price', 'rental_income',
    #                                  'units', 'rental_growth',
    #                                  'capital_gain', 'downpayment', 'loan_length', 'interest_rate', 'insurance',
    #                                  'prop_tax', 'capex', 'vacancy', 'repairs_maintain'
    #                                ,'management_fee', 'expense_growth', 'cash_on_cash_return', 'mon_income_unit'])
    # st.dataframe(clean_db)
    unique_list = [i[0] for i in view_all_titles()]
    st.write(unique_list)
    delete_by_title = st.selectbox("Select Property", unique_list)
    to_delete = get_single_property(delete_by_title)
    for i in to_delete:
        # short_article = str(i[1])[0:50]
        # st.write(to_delete)
        st.write(head_message_temp.format(i[2], i[1], i[3], i[6], round(float(i[19]),2)), unsafe_allow_html=True)

    if st.button("Delete"):
        delete_data(delete_by_title)
        st.warning("Deleted: '{}'".format(delete_by_title))

elif choice == "Edit Properties":
    st.header("Edit Property")

    # clean_db = pd.DataFrame(result,
    #                         columns=['property_address','url', 'propery_image', 'purch_price', 'rental_income',
    #                                  'units', 'rental_growth',
    #                                  'capital_gain', 'downpayment', 'loan_length', 'interest_rate', 'insurance',
    #                                  'prop_tax', 'capex', 'vacancy', 'repairs_maintain'
    #                             , 'management_fee', 'expense_growth', 'cash_on_cash_return', 'mon_income_unit'])
    # st.dataframe(clean_db)

    with st.sidebar:
        # with st.form(key='my_form1'):
            result = view_all_notes()
            unique_list = [i[0] for i in view_all_titles()]
            edit_by_address = st.sidebar.selectbox("Select Property", unique_list)
            # if st.form_submit_button(label='Load'):


    # if st.sidebar.button("Load"):
    saved_info = get_single_property(edit_by_address)
#     st.info("Property Edited: '{}'".format(edit_by_address))
    init_url = saved_info[0][0]
    init_propery_image = saved_info[0][1]
    init_property_address = saved_info[0][2]
    init_purch_price = saved_info[0][3]
    init_rental_income = saved_info[0][4]
    init_units = saved_info[0][5]
    init_rental_growth = saved_info[0][6]
    init_capital_gain = saved_info[0][7]
    init_downpayment = saved_info[0][8]
    init_loan_length = saved_info[0][9]
    init_interest_rate = saved_info[0][10]
    init_insurance = saved_info[0][11]
    init_prop_tax = saved_info[0][12]
    init_capex = saved_info[0][13]
    init_vacancy = saved_info[0][14]
    init_repairs_maintain = saved_info[0][15]
    init_management_fee = saved_info[0][16]
    init_expense_growth = saved_info[0][17]
    init_rehab_costs = 0

    property_info = [init_property_address, init_url, init_propery_image, init_purch_price, init_rental_income,init_units, init_rental_growth,
    init_capital_gain, init_downpayment, init_loan_length, init_interest_rate, init_insurance,init_prop_tax, init_capex, init_vacancy,
    init_repairs_maintain, init_management_fee, init_expense_growth, init_rehab_costs]
    # st.write(property_info)

    calculate_results(property_info, True)
    # st.write(updated)

    # st.write((updated_info))
    # if st.button("Update Property"):
    #     # st.write(new_property_info)
    #     st.write(updated)
    #     delete_data(updated)
    #     add_data(updated)
    #
    #
    #     st.success("{} saved".format(property_info[0]))


# if __name__ == '__main__':
#     main()
