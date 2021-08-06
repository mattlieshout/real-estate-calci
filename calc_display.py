import sqlite3
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
# from functions import *


conn = sqlite3.connect("data.db")
c = conn.cursor()


def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS blogtable(property_address TEXT, url TEXT, propery_image TEXT, 
            purch_price TEXT, rental_income TEXT, units TEXT, rental_growth TEXT, capital_gain TEXT, downpayment TEXT, loan_length TEXT, interest_rate TEXT, insurance TEXT,
            prop_tax TEXT, capex TEXT, vacancy TEXT, repairs_maintain TEXT, management_fee TEXT, expense_growth TEXT, cash_on_cash_return TEXT, mon_income_unit TEXT)''')


create_table()


def add_data(property_info):
    c.execute('''INSERT INTO blogtable ('property_address', 'url', 'propery_image', 'purch_price', 'rental_income', 'units', 'rental_growth',
                     'capital_gain', 'downpayment','loan_length','interest_rate','insurance','prop_tax','capex','vacancy','repairs_maintain'
                     ,'management_fee','expense_growth','cash_on_cash_return', 'mon_income_unit') VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                    (property_info[0], property_info[1], property_info[2], property_info[3], property_info[4], property_info[5], property_info[6], property_info[7],
                     property_info[8], property_info[9],property_info[10],property_info[11],property_info[12],property_info[13],property_info[14],property_info[15],property_info[16]
                     ,property_info[17], property_info[18], property_info[19]))
    conn.commit()



def view_all_notes():
    c.execute('SELECT * FROM blogtable')
    data = c.fetchall()
    return data


def view_all_titles():
    c.execute('SELECT DISTINCT property_address FROM blogtable')
    data = c.fetchall()
    # for row in data:
    #   print(row)
    return data


def get_single_property(property_address):
    c.execute('SELECT * FROM blogtable WHERE property_address="{}"'.format(property_address))
    data = c.fetchall()
    return data


def get_blog_by_property_address(property_address):
    c.execute('SELECT * FROM blogtable WHERE property_address="{}"'.format(property_address))
    data = c.fetchall()
    return data

#
# def get_blog_by_author(author):
#     c.execute('SELECT * FROM blogtable WHERE author="{}"'.format(author))
#     data = c.fetchall()
#     return data

#
# def get_blog_by_msg(article):
#     c.execute("SELECT * FROM blogtable WHERE article like '%{}%'".format(article))
#     data = c.fetchall()
#     return data


def edit_blog_author(author, new_author):
    c.execute('UPDATE blogtable SET author ="{}" WHERE author="{}"'.format(new_author, author))
    conn.commit()
    data = c.fetchall()
    return data

#
# def edit_property(property_info):
#     st.write(property_info)
#     # c.execute('UPDATE blogtable SET property_address ="{}" WHERE property_address="{}"'.format(property_address, property_address))
#     conn.commit()
#     data = c.fetchall()
#     return data

#
# def edit_blog_article(article, new_article):
#     c.execute('UPDATE blogtable SET property_address ="{}" WHERE property_address="{}"'.format(new_article, article
#                                                                          ))
#     conn.commit()
#     data = c.fetchall()
#     return data


def delete_data(property_address):
    c.execute('DELETE FROM blogtable WHERE property_address="{}"'.format(property_address))
    conn.commit()
#

############################ Calculate Results ###################################


def calculate_results(property_info,edit):
    with st.sidebar:
        # with st.form(key='my_form'):
        st.header("Basic Information")
        property_address = st.text_input("Enter the Property Address:   ", value=str(property_info[0]))
        # st.write(property_address)

        url = st.text_input("Enter the listing url from Realtor:   ", value=str(property_info[1]))
        propery_image = st.text_input("Image url:   ",
                                              value=str(property_info[2]))
        st.header("Income")
        purch_price = float(st.text_input("Enter the Property Cost:   ", value=str(property_info[3])))
        rehab_costs = float(st.text_input("Enter the Rehab Cost:   ", value=str(property_info[4])))
        rental_income = float(st.text_input("Enter the Monthly Rent:   ", value=str(property_info[5])))
        units = int(
            st.slider("Number of Units", min_value=int(1), max_value=int(4), value=int(property_info[6]),
                              step=int(1)))
        rental_growth = st.slider("Rental Income Growth (%)", min_value=0.0, max_value=10.0,
                                          value=float(property_info[7]), step=0.5)
        capital_gain = st.slider("Capital Appreciation (%)", min_value=0.0, max_value=10.0,
                                         value=float(property_info[8]), step=0.5)
        st.subheader("Loan Information")
        downpayment = st.slider("Downpayment (%)", min_value=0.0, max_value=100.0,
                                        value=float(property_info[9]),
                                        step=0.5)
        loan_length = st.slider("Loan Length", min_value=0, max_value=30, value=int(property_info[10]), step=1)
        interest_rate = st.slider("Interest Rate (%)", min_value=0.00, max_value=10.00,
                                          value=float(property_info[11]), step=0.01)
        st.subheader("Expenses")
        insurance = float(st.text_input("Enter the insurance cost:   ", value=property_info[12]))
        prop_tax = float(st.text_input("Enter the property tax:   ", value=property_info[13]))
        capex = st.slider("Capital Expenditure (%)", min_value=0, max_value=10, value=int(property_info[14]))
        vacancy = st.slider("Vacancy", min_value=0, max_value=10, value=int(property_info[15]))
        repairs_maintain = st.slider("Repairs and Maintenance", min_value=0, max_value=10,
                                             value=int(property_info[16]))
        management_fee = st.slider("Management Fee", min_value=0, max_value=15, value=int(float(property_info[17])))
        expense_growth = st.slider("Expense Growth", min_value=0.0, max_value=10.0,
                                           value=float(property_info[18]),
                                           step=0.5)
        new_property_info = [property_address, url, propery_image, purch_price,rehab_costs,rental_income,units,rental_growth,capital_gain,downpayment,loan_length,interest_rate,insurance,prop_tax,capex,vacancy,repairs_maintain,management_fee,expense_growth]

            # if st.form_submit_button(label='Calculate'):
            #     st.success("Calculation Complete")
    st.write("""
            # Property Investment Analysis
            """)
    # st.write(new_property_info)
    st.write(new_property_info[0])
    st.write('---')
    st.image(new_property_info[2])
    st.write('---')
    # Sidebar
    # Header of Specify Input Parameters
    # st.sidebar.header('S')

    ###### Creating lists ######
    payment_number = []
    loan_beg_bal = []
    pay = []
    principal = []
    interest_to_pay = []
    end_bal = []
    prop_val = []
    monthly_income = []
    monthly_expenses = []
    monthly_profit = []
    equity_in_property = []

    ######### Initial Calculations #############
    purchase_price = new_property_info[3] + new_property_info[4]
    inital_loan_amount = float(purchase_price - (purchase_price * (new_property_info[9] / 100)))
    downpayment_dollar = purchase_price - inital_loan_amount
    monthly_interest_rate = float(new_property_info[11] / 12) / 100
    mon_pay = int(
        inital_loan_amount * monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** (-1 * new_property_info[10] * 12)))
    yearly_expenses = mon_pay * 12 + new_property_info[12] + new_property_info[13] + new_property_info[5] * (
            new_property_info[14] / 100 + new_property_info[15] / 100 + new_property_info[16] / 100 + new_property_info[17] / 100) * 12
    cash_on_cash_return = (new_property_info[5] * 12 - yearly_expenses) / (downpayment_dollar) * 100
    mon_income_unit = (new_property_info[5] * 12 - yearly_expenses) / new_property_info[6] / 12
    new_property_info.append(cash_on_cash_return)
    new_property_info.append(mon_income_unit)

    # st.write(price_mine(url))
    # st.write(monthly_interest_rate)
    st.write("Purchase Price: $", f'{purchase_price:,.2f}')
    st.write("Beginning Loan Amount: $", f'{inital_loan_amount:,.2f}')
    st.write("Downpayment Amount: $", f'{downpayment_dollar:,.2f}')
    st.write("Monthly Payments: $", f'{mon_pay:,.2f}')
    st.write("Cash on Cash Return: ", f'{cash_on_cash_return:,.2f} %')
    st.write("Yearly Income: $", f'{new_property_info[5] * 12 - yearly_expenses:,.2f}')
    st.write("Income/Unit/Month: $", f'{mon_income_unit:,.2f}')

    for n in range(0, (new_property_info[10] * 12)):
        if n == 0:
            payment_number.append(n)
            pay.append(float(inital_loan_amount * monthly_interest_rate / (
                    1 - (1 + monthly_interest_rate) ** (-1 * new_property_info[10] * 12))))
            loan_beg_bal.append(float(inital_loan_amount))
            interest_to_pay.append(float(inital_loan_amount * monthly_interest_rate))
            principal.append(pay[n] - interest_to_pay[n])
            end_bal.append(loan_beg_bal[n] - principal[n])
            prop_val.append(purchase_price)
            monthly_income.append(new_property_info[5])
            monthly_expenses.append((pay[n] + (new_property_info[12] + new_property_info[13]) / 12 + monthly_income[n] * new_property_info[14] / 100 +
                                     monthly_income[n] * new_property_info[15] / 100 + monthly_income[
                                         n] * new_property_info[16] / 100 + monthly_income[n] * new_property_info[17] / 100) * (
                                            1 + (new_property_info[18] / 100)))
            monthly_profit.append(monthly_income[n] - monthly_expenses[n])
            equity_in_property.append(prop_val[n] + monthly_profit[n] - end_bal[n])
        else:
            payment_number.append(n)
            pay.append(float(
                inital_loan_amount * monthly_interest_rate / (
                        1 - (1 + monthly_interest_rate) ** (-1 * new_property_info[10] * 12))))
            loan_beg_bal.append(float(end_bal[n - 1]))
            interest_to_pay.append(float(loan_beg_bal[n] * monthly_interest_rate))
            principal.append(pay[n] - interest_to_pay[n])
            end_bal.append(loan_beg_bal[n] - principal[n])
            prop_val.append(prop_val[n - 1] * (1 + (new_property_info[8] / 100 / 12)))
            monthly_income.append(monthly_income[n - 1] * (1 + (new_property_info[7] / 100 / 12)))
            monthly_expenses.append((monthly_expenses[n - 1]) * (1 + (new_property_info[18]/ 1200)))
            monthly_profit.append(monthly_income[n] - monthly_expenses[n])
            equity_in_property.append(
                equity_in_property[n - 1] + monthly_profit[n] + (prop_val[n] - prop_val[n - 1]))



    df = pd.DataFrame(
        {
            'Payment Number': payment_number,
            'Beginning Balance of Loan': loan_beg_bal,
            'Equity in Property': equity_in_property
        },
        columns=['Payment Number', 'Beginning Balance of Loan', 'Equity in Property']
    )

    df = df.melt('Payment Number', var_name='Legend', value_name='Dollars ($)')

    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('Payment Number'),
        y=alt.Y('Dollars ($):Q'),
        color=alt.Color("Legend:N")
    ).properties(title="Equity in Property")
    st.altair_chart(chart, use_container_width=True)

    df2 = pd.DataFrame(
        {
            'Payment Number': payment_number,
            'Monthly Income': monthly_income,
            'Monthly Expenses': monthly_expenses,
        },
        columns=['Payment Number', 'Monthly Income', 'Monthly Expenses']
    )

    df2 = df2.melt('Payment Number', var_name='Legend', value_name='Dollars ($)')

    chart = alt.Chart(df2).mark_line().encode(
        x=alt.X('Payment Number'),
        y=alt.Y('Dollars ($):Q'),
        color=alt.Color("Legend:N")
    ).properties(title="Monthly Inflows and Outflows")
    st.altair_chart(chart, use_container_width=True)
    dfc = pd.DataFrame({
        # 'Payment Date': payment_number,
        'Loan Begin Bal': loan_beg_bal,
        'Payment': pay,
        'Interest': interest_to_pay,
        'Principal': principal,
        'Ending Balance': end_bal,
        'Property Value': prop_val,
        'Monthly Income': monthly_income,
        'Monthly Expenses': monthly_expenses,
        'Monthly Profit': monthly_profit,
        'Equity in Property': equity_in_property,
    })

    st.write(dfc)
    # st.write(new_property_info)
    if edit:
        if st.button("Update Property"):
            st.write(new_property_info[0])
            # st.write(new_property_info)
            delete_data(new_property_info[0])
            add_data(new_property_info)

            st.success("{} Updated".format(property_info[0]))
        return
    else:
        if st.button("Save New Property"):
            st.write(new_property_info[0])
            delete_data(new_property_info[0])
            add_data(new_property_info)

            st.success("{} saved".format(new_property_info[0]))
        return
