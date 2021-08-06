# import streamlit as st
# import pandas as pd
# import altair as alt
# import shap
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn import datasets
# from sklearn.ensemble import RandomForestRegressor
# from requests import get
# from bs4 import BeautifulSoup
# from functions import *
#
#
# # def price_mine(url):
# #     # Currently this function takes an input of a URL and returns the listing prices
# #     response = get(url)
# #     response_text = response.text
# #     html_soup = BeautifulSoup(response_text, 'html.parser')
# #     prices = html_soup.find(class_="bVPpjr")
# #     return prices
#
# avatar1 = "https://www.w3schools.com/howto/img_avatar1.png"
# avatar2 = "https://www.w3schools.com/howto/img_avatar2.png"
#
# title_temp = """
# 	<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
# 	<h4 style="color:white;text-align:center;">{}</h1>
# 	<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
# 	<h6>Author:{}</h6>
# 	<br/>
# 	<br/>
# 	<p style="text-align:justify">{}</p>
# 	</div>
# 	"""
# article_temp = """
# 	<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
# 	<h4 style="color:white;text-align:center;">{}</h1>
# 	<h6>Author:{}</h6>
# 	<h6>Post Date: {}</h6>
# 	<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;width: 50px;height: 50px;" >
# 	<br/>
# 	<br/>
# 	<p style="text-align:justify">{}</p>
# 	</div>
# 	"""
# head_message_temp = """
# 	<div style="background-color:white;padding:10px;border-radius:5px;margin:10px;border-style: solid;border-color: gray;">
# 	<h4 style="color:gray;text-align:Left;">Address: {}</h1>
# 	<img src="{}" alt="Avatar" style="vertical-align: center;float:right;max-height: 130px"; padding:10px>
# 	<h6>Purchase Price: ${}</h6>
# 	<h6>Number of Units: {}</h6>
# 	<h6>Cash on Cash Return: {}%</h6>
# 	<h6>Income/Unit/Month: ${}</h6>
# 	</div>
# 	"""
# full_message_temp = """
# 	<div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
# 		<p style="text-align:justify;color:black;padding:10px">{}</p>
# 	</div>
# 	"""
#
# HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""
#
#
#
#
# def edit_property(init_trial, init_propery_image, init_property_address, init_purch_price, init_rental_income,
#                       init_units,
#                       init_rental_growth,
#                       init_capital_gain, init_downpayment, init_loan_length, init_interest_rate, init_insurance,
#                       init_prop_tax, init_capex, init_vacancy,
#                       init_repairs_maintain, init_management_fee, init_expense_growth, init_rehab_costs):
#         rehab_costs = 0
#
# ##### INPUTS #######
#     with st.sidebar():
#         with st.form(key='form1'):
#             st.header("Basic Information")
#             property_address = st.sidebar.text_input("Enter the Property Address:   ", value=str(init_property_address))
#             trial = st.sidebar.text_input("Enter the listing URL from Realtor:   ", value=str(init_trial))
#             propery_image = st.sidebar.text_input("Image URL:   ",
#                                                   value=str(init_propery_image))
#             st.sidebar.header("Income")
#             purch_price = float(st.sidebar.text_input("Enter the Property Cost:   ", value=str(init_purch_price)))
#             if st.sidebar.checkbox("Rehab Costs"):
#                 rehab_costs = float(st.sidebar.text_input("Enter the Rehab Cost:   ", value=str(init_rehab_costs)))
#             rental_income = float(st.sidebar.text_input("Enter the Monthly Rent:   ", value=str(init_rental_income)))
#             units = int(
#                 st.sidebar.slider("Number of Units", min_value=int(1), max_value=int(4), value=int(init_units), step=int(1)))
#             rental_growth = st.sidebar.slider("Rental Income Growth (%)", min_value=0.0, max_value=10.0,
#                                               value=float(init_rental_growth), step=0.5)
#             capital_gain = st.sidebar.slider("Capital Appreciation (%)", min_value=0.0, max_value=10.0,
#                                              value=float(init_capital_gain), step=0.5)
#             st.sidebar.subheader("Loan Information")
#             downpayment = st.sidebar.slider("Downpayment (%)", min_value=0.0, max_value=100.0, value=float(init_downpayment),
#                                             step=0.5)
#             loan_length = st.sidebar.slider("Loan Length", min_value=0, max_value=30, value=int(init_loan_length), step=1)
#             interest_rate = st.sidebar.slider("Interest Rate (%)", min_value=0.00, max_value=10.00,
#                                               value=float(init_interest_rate), step=0.01)
#             st.sidebar.subheader("Expenses")
#             insurance = float(st.sidebar.text_input("Enter the insurance cost:   ", value=init_insurance))
#             prop_tax = float(st.sidebar.text_input("Enter the property tax:   ", value=init_prop_tax))
#             capex = st.sidebar.slider("Capital Expenditure (%)", min_value=0, max_value=10, value=int(init_capex))
#             vacancy = st.sidebar.slider("Vacancy", min_value=0, max_value=10, value=int(init_vacancy))
#             repairs_maintain = st.sidebar.slider("Repairs and Maintenance", min_value=0, max_value=10,
#                                                  value=int(init_repairs_maintain))
#             management_fee = st.sidebar.slider("Management Fee", min_value=0, max_value=15, value=int(init_management_fee))
#             expense_growth = st.sidebar.slider("Expense Growth", min_value=0.0, max_value=10.0,
#                                                value=float(init_expense_growth),
#                                                step=0.5)
#             if st.form_submit_button(label='calculate'):
#                 st.success("Calculation Complete")
#
#     st.write("""
#         # Property Investment Analysis
#         """)
#     st.write(property_address)
#     st.write('---')
#     st.image(propery_image)
#     st.write('---')
#     # Sidebar
#     # Header of Specify Input Parameters
#     # st.sidebar.header('S')
#
#     create_table()
#
#     ###### Creating lists ######
#     payment_number = []
#     loan_beg_bal = []
#     pay = []
#     principal = []
#     interest_to_pay = []
#     end_bal = []
#     prop_val = []
#     monthly_income = []
#     monthly_expenses = []
#     monthly_profit = []
#     equity_in_property = []
#
#     ######### Initial Calculations #############
#     purchase_price = purch_price + rehab_costs
#     inital_loan_amount = float(purchase_price - (purchase_price * (downpayment / 100)))
#     downpayment_dollar = purchase_price - inital_loan_amount
#     monthly_interest_rate = float(interest_rate / 12) / 100
#     mon_pay = int(
#         inital_loan_amount * monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** (-1 * loan_length * 12)))
#     yearly_expenses = mon_pay * 12 + insurance + prop_tax + rental_income * (
#             capex / 100 + vacancy / 100 + repairs_maintain / 100 + management_fee / 100) * 12
#     cash_on_cash_return = (rental_income * 12 - yearly_expenses) / (downpayment_dollar) * 100
#     mon_income_unit = (rental_income * 12 - yearly_expenses) / units / 12
#
#     # st.write(price_mine(trial))
#     # st.write(monthly_interest_rate)
#     st.write("Purchase Price: $", f'{purchase_price:,.2f}')
#     st.write("Beginning Loan Amount: $", f'{inital_loan_amount:,.2f}')
#     st.write("Downpayment Amount: $", f'{downpayment_dollar:,.2f}')
#     st.write("Monthly Payments: $", f'{mon_pay:,.2f}')
#     st.write("Cash on Cash Return: ", f'{cash_on_cash_return:,.2f} %')
#     st.write("Yearly Income: $", f'{rental_income * 12 - yearly_expenses:,.2f}')
#     st.write("Income/Unit/Month: $", f'{mon_income_unit:,.2f}')
#
#     ## Create list of length from years entered
#     for n in range(0, (loan_length * 12)):
#         if n == 0:
#             payment_number.append(n)
#             pay.append(float(inital_loan_amount * monthly_interest_rate / (
#                     1 - (1 + monthly_interest_rate) ** (-1 * loan_length * 12))))
#             loan_beg_bal.append(float(inital_loan_amount))
#             interest_to_pay.append(float(inital_loan_amount * monthly_interest_rate))
#             principal.append(pay[n] - interest_to_pay[n])
#             end_bal.append(loan_beg_bal[n] - principal[n])
#             prop_val.append(purchase_price)
#             monthly_income.append(rental_income)
#             monthly_expenses.append((pay[n] + (insurance + prop_tax) / 12 + monthly_income[n] * capex / 100 +
#                                      monthly_income[n] * vacancy / 100 + monthly_income[
#                                          n] * repairs_maintain / 100 + monthly_income[n] * management_fee / 100) * (
#                                             1 + (expense_growth / 100)))
#             monthly_profit.append(monthly_income[n] - monthly_expenses[n])
#             equity_in_property.append(prop_val[n] + monthly_profit[n] - end_bal[n])
#         else:
#             payment_number.append(n)
#             pay.append(float(
#                 inital_loan_amount * monthly_interest_rate / (
#                         1 - (1 + monthly_interest_rate) ** (-1 * loan_length * 12))))
#             loan_beg_bal.append(float(end_bal[n - 1]))
#             interest_to_pay.append(float(loan_beg_bal[n] * monthly_interest_rate))
#             principal.append(pay[n] - interest_to_pay[n])
#             end_bal.append(loan_beg_bal[n] - principal[n])
#             prop_val.append(prop_val[n - 1] * (1 + (capital_gain / 100 / 12)))
#             monthly_income.append(monthly_income[n - 1] * (1 + (rental_growth / 100 / 12)))
#             monthly_expenses.append((monthly_expenses[n - 1]) * (1 + (expense_growth / 1200)))
#             monthly_profit.append(monthly_income[n] - monthly_expenses[n])
#             equity_in_property.append(
#                 equity_in_property[n - 1] + monthly_profit[n] + (prop_val[n] - prop_val[n - 1]))
#
#     dfc = pd.DataFrame({
#         # 'Payment Date': payment_number,
#         'Loan Begin Bal': loan_beg_bal,
#         'Payment': pay,
#         'Interest': interest_to_pay,
#         'Principal': principal,
#         'Ending Balance': end_bal,
#         'Property Value': prop_val,
#         'Monthly Income': monthly_income,
#         'Monthly Expenses': monthly_expenses,
#         'Monthly Profit': monthly_profit,
#         'Equity in Property': equity_in_property,
#     })
#
#     st.write(dfc)
#
#     df = pd.DataFrame(
#         {
#             'Payment Number': payment_number,
#             'Beginning Balance of Loan': loan_beg_bal,
#             'Equity in Property': equity_in_property
#         },
#         columns=['Payment Number', 'Beginning Balance of Loan', 'Equity in Property']
#     )
#
#     df = df.melt('Payment Number', var_name='Legend', value_name='Dollars ($)')
#
#     chart = alt.Chart(df).mark_line().encode(
#         x=alt.X('Payment Number'),
#         y=alt.Y('Dollars ($):Q'),
#         color=alt.Color("Legend:N")
#     ).properties(title="Equity in Property")
#     st.altair_chart(chart, use_container_width=True)
#
#     df2 = pd.DataFrame(
#         {
#             'Payment Number': payment_number,
#             'Monthly Income': monthly_income,
#             'Monthly Expenses': monthly_expenses,
#         },
#         columns=['Payment Number', 'Monthly Income', 'Monthly Expenses']
#     )
#
#     df2 = df2.melt('Payment Number', var_name='Legend', value_name='Dollars ($)')
#
#     chart = alt.Chart(df2).mark_line().encode(
#         x=alt.X('Payment Number'),
#         y=alt.Y('Dollars ($):Q'),
#         color=alt.Color("Legend:N")
#     ).properties(title="Monthly Inflows and Outflows")
#     st.altair_chart(chart, use_container_width=True)
#
#     if st.button("Save New Property"):
#         add_data(trial, propery_image, property_address, purch_price, rental_income, units, rental_growth,
#                  capital_gain, downpayment, loan_length, interest_rate, insurance, prop_tax, capex, vacancy,
#                  repairs_maintain
#                  , management_fee, expense_growth, cash_on_cash_return, mon_income_unit)
#         st.success("{} saved".format(property_address))
#
#
# def main():
#     html_temp = """
#     		<div style="background-color:{};padding:10px;border-radius:5px">
#     		<h1 style="color:{};text-align:center;">Property Analyzer </h1>
#     		</div>
#     		"""
#     st.markdown(html_temp.format('gray', 'white'), unsafe_allow_html=True)
#     menu = ["Home", "Add New Property", "Saved Properties", "Search", "Edit Properties", "Delete Properties"]
#
#     choice = st.sidebar.selectbox("Menu", menu)
#
#     if choice == "Home":
#         st.subheader("Home")
#         result = view_all_notes()
#         for i in result:
#             short_article = str(i[2])[0:50]
#             st.write(head_message_temp.format(i[2], i[1], i[3], i[5], i[18], i[19]), unsafe_allow_html=True)
#
#
#     elif choice == "Add New Property":
#         init_trial = "https://www.realtor.com/"
#         init_propery_image = "https://lh3.googleusercontent.com/proxy/zLpbQxQ8UEcm8VJSP7FnfHG33ER4EvVUKQ25GcELWgAXyMwnxugZS66Tf9k925Px_WEU55IcFP1wJOrBh9j1170ZpWjk0eyNmb0aozlcKiNR0jhrPZu7Dh01l2xxr-JT1jOvnEOUm8RNVE9NC0tjbmGdK2xUa2kR_mWEzKhaubfV_N8KBvaMnGLGfg"
#         init_property_address = "Enter Address"
#         init_purch_price = 800000
#         init_rehab_costs = 0
#         init_rental_income = 4000
#         init_units = 2
#         init_rental_growth = 2.0
#         init_capital_gain = 2.0
#         init_downpayment = 5.0
#         init_loan_length = 30
#         init_interest_rate = 3.0
#         init_insurance = 2000
#         init_prop_tax = 10000
#         init_capex = 5
#         init_vacancy = 5
#         init_repairs_maintain = 5
#         init_management_fee = 8
#         init_expense_growth = 2.0
#         init_rehab_costs = 0
#         edit_property(init_trial, init_propery_image, init_property_address, init_purch_price, init_rental_income,
#                       init_units, init_rental_growth,
#                       init_capital_gain, init_downpayment, init_loan_length, init_interest_rate, init_insurance,
#                       init_prop_tax, init_capex, init_vacancy,
#                       init_repairs_maintain, init_management_fee, init_expense_growth, init_rehab_costs)
#
#
#     elif choice == "Saved Properties":
#         st.subheader("Saved Properties")
#         all_titles = [i[0] for i in view_all_titles()]
#         postlist = st.sidebar.selectbox("Posts", all_titles)
#         post_result = get_blog_by_property_address(postlist)
#         for i in post_result:
#             st.markdown(head_message_temp.format(i[2], i[1], i[3], i[5], i[18], i[19]), unsafe_allow_html=True)
#             # st.markdown(full_message_temp.format(i[2]), unsafe_allow_html=True)
#
#     elif choice == "Search":
#         st.subheader("Search")
#         st.subheader("Search Properties")
#         search_term = st.text_input("Enter Term")
#         search_choice = "Address"
#         if st.button('Search'):
#             if search_choice == "Address":
#                 article_result = get_blog_by_property_address(search_term)
#             # elif search_choice == "author":
#             #     article_result = get_blog_by_author(search_term)
#
#             # Preview Articles
#             for i in article_result:
#                 # st.text("Reading Time:{} minutes".format(readingTime(str(i[2]))))
#                 # st.write(article_temp.format(i[1],i[0],i[3],i[2]),unsafe_allow_html=True)
#                 st.write(head_message_temp.format(i[2], i[1], i[3], i[5], i[18], i[19]), unsafe_allow_html=True)
#                 st.write(full_message_temp.format(i[2]), unsafe_allow_html=True)
#
#     elif choice == "Delete Properties":
#         st.subheader("Delete Properties")
#         result = view_all_notes()
#         clean_db = pd.DataFrame(result,
#                                 columns=['trial', 'propery_image', 'property_address', 'purch_price', 'rental_income',
#                                          'units', 'rental_growth',
#                                          'capital_gain', 'downpayment', 'loan_length', 'interest_rate', 'insurance',
#                                          'prop_tax', 'capex', 'vacancy', 'repairs_maintain'
#                                     , 'management_fee', 'expense_growth', 'cash_on_cash_return', 'mon_income_unit'])
#         st.dataframe(clean_db)
#         unique_list = [i[0] for i in view_all_titles()]
#         delete_by_title = st.selectbox("Select Property", unique_list)
#         if st.button("Delete"):
#             delete_data(delete_by_title)
#             st.warning("Deleted: '{}'".format(delete_by_title))
#
#     elif choice == "Edit Properties":
#         st.subheader("Edit Properties")
#
#         result = view_all_notes()
#         clean_db = pd.DataFrame(result,
#                                 columns=['trial', 'propery_image', 'property_address', 'purch_price', 'rental_income',
#                                          'units', 'rental_growth',
#                                          'capital_gain', 'downpayment', 'loan_length', 'interest_rate', 'insurance',
#                                          'prop_tax', 'capex', 'vacancy', 'repairs_maintain'
#                                     , 'management_fee', 'expense_growth', 'cash_on_cash_return', 'mon_income_unit'])
#         st.dataframe(clean_db)
#         unique_list = [i[0] for i in view_all_titles()]
#         edit_by_address = st.selectbox("Select Property", unique_list)
#         if st.button("Edit"):
#             saved_info = get_single_property(edit_by_address)
#             st.info("Property Edited: '{}'".format(edit_by_address))
#             init_trial = saved_info[0][0]
#             init_propery_image = saved_info[0][1]
#             init_property_address = saved_info[0][2]
#             init_purch_price = saved_info[0][3]
#             init_rental_income = saved_info[0][4]
#             init_units = saved_info[0][5]
#             init_rental_growth = saved_info[0][6]
#             init_capital_gain = saved_info[0][7]
#             init_downpayment = saved_info[0][8]
#             init_loan_length = saved_info[0][9]
#             init_interest_rate = saved_info[0][10]
#             init_insurance = saved_info[0][11]
#             init_prop_tax = saved_info[0][12]
#             init_capex = saved_info[0][13]
#             init_vacancy = saved_info[0][14]
#             init_repairs_maintain = saved_info[0][15]
#             init_management_fee = saved_info[0][16]
#             init_expense_growth = saved_info[0][17]
#             init_rehab_costs = 0
#             edit_property(init_trial, init_propery_image, init_property_address, init_purch_price, init_rental_income,
#                           init_units, init_rental_growth,
#                           init_capital_gain, init_downpayment, init_loan_length, init_interest_rate, init_insurance,
#                           init_prop_tax, init_capex, init_vacancy,
#                           init_repairs_maintain
#                           , init_management_fee, init_expense_growth, init_rehab_costs)
#
#
# if __name__ == '__main__':
#     main()
