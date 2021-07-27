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

def price_mine(url):
    # Currently this function takes an input of a URL and returns the listing prices
    response = get(url)
    response_text = response.text
    html_soup = BeautifulSoup(response_text, 'html.parser')
    prices = html_soup.find(class_="bVPpjr")
    return prices





##### INPUTS #######
st.sidebar.header("Basic Information")
property_address = st.sidebar.text_input("Enter the Property Address:   ")
trial = st.sidebar.text_input("Enter the listing URL from Realtor:   ", value="https://www.realtor.com/")
propery_image = st.sidebar.text_input("Image URL:   ", value="https://lh3.googleusercontent.com/proxy/zLpbQxQ8UEcm8VJSP7FnfHG33ER4EvVUKQ25GcELWgAXyMwnxugZS66Tf9k925Px_WEU55IcFP1wJOrBh9j1170ZpWjk0eyNmb0aozlcKiNR0jhrPZu7Dh01l2xxr-JT1jOvnEOUm8RNVE9NC0tjbmGdK2xUa2kR_mWEzKhaubfV_N8KBvaMnGLGfg")
st.sidebar.header("Income")
purch_price = float(st.sidebar.text_input("Enter the Property Cost:   ", value="800000"))
if st.sidebar.checkbox("Rehab Costs"):
    rehab_costs = float(st.sidebar.text_input("Enter the Rehab Cost:   ", value="0"))
rental_income = float(st.sidebar.text_input("Enter the Monthly Rent:   ", value="4000"))
units = int(st.sidebar.slider("Number of Units", min_value=1.0, max_value=4.0, value=2.0, step=1.0))
rental_growth = st.sidebar.slider("Rental Income Growth (%)", min_value=0.0, max_value=10.0, value=2.0, step=0.5)
capital_gain = st.sidebar.slider("Capital Appreciation (%)", min_value=0.0, max_value=10.0, value=2.0, step=0.5)
st.sidebar.subheader("Loan Information")
downpayment = st.sidebar.slider("Downpayment (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.5)
loan_length = st.sidebar.slider("Loan Length", min_value=0, max_value=30, value=30)
interest_rate = st.sidebar.slider("Interest Rate (%)", min_value=0.00, max_value=10.00, value=3.00, step=0.01)
st.sidebar.subheader("Expenses")
insurance = float(st.sidebar.text_input("Enter the insurance cost:   ", value="1000"))
prop_tax = float(st.sidebar.text_input("Enter the property tax:   ", value="1000"))
capex = st.sidebar.slider("Capital Expenditure (%)", min_value=0, max_value=10, value=5)
vacancy = st.sidebar.slider("Vacancy", min_value=0, max_value=10, value=5)
repairs_maintain = st.sidebar.slider("Repairs and Maintenance", min_value=0, max_value=10, value=5)
management_fee = st.sidebar.slider("Management Fee", min_value=0, max_value=15, value=10)
expense_growth = st.sidebar.slider("Expense Growth", min_value=0.0, max_value=10.0, value=2.0, step=0.5)


st.write("""
# Property Investment Analysis
""")
st.write(property_address)
st.write('---')
st.image(propery_image)
st.write('---')
# Sidebar
# Header of Specify Input Parameters
# st.sidebar.header('S')

rehab_costs = 0



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
purchase_price = purch_price + rehab_costs
inital_loan_amount = float(purchase_price-(purchase_price*(downpayment/100)))
downpayment_dollar = purchase_price-inital_loan_amount
monthly_interest_rate = float(interest_rate/12)/100
mon_pay = int(inital_loan_amount*monthly_interest_rate/(1-(1+monthly_interest_rate)**(-1*loan_length*12)))
yearly_expenses = mon_pay*12 + insurance + prop_tax + rental_income*(capex/100 + vacancy/100 + repairs_maintain/100 + management_fee/100)*12
cash_on_cash_return = (rental_income*12 - yearly_expenses)/(downpayment_dollar)*100

# st.write(price_mine(trial))
# st.write(monthly_interest_rate)
st.write("Purchase Price: $", f'{purchase_price:,.2f}')
st.write("Beginning Loan Amount: $", f'{inital_loan_amount:,.2f}')
st.write("Downpayment Amount: $", f'{downpayment_dollar:,.2f}')
st.write("Monthly Payments: $", f'{mon_pay:,.2f}')
st.write("Cash on Cash Return: ", f'{cash_on_cash_return:,.2f} %')
st.write("Yearly Income: $", f'{rental_income*12 - yearly_expenses:,.2f}')
st.write("Income/Unit/Month: $", f'{(rental_income*12-yearly_expenses)/units/12:,.2f}')

## Create list of length from years entered
for n in range(0, (loan_length*12)):
    if n == 0:
        payment_number.append(n)
        pay.append(float(inital_loan_amount*monthly_interest_rate/(1-(1+monthly_interest_rate)**(-1*loan_length*12))))
        loan_beg_bal.append(float(inital_loan_amount))
        interest_to_pay.append(float(inital_loan_amount*monthly_interest_rate))
        principal.append(pay[n] - interest_to_pay[n])
        end_bal.append(loan_beg_bal[n]-principal[n])
        prop_val.append(purchase_price)
        monthly_income.append(rental_income)
        monthly_expenses.append((pay[n] + (insurance + prop_tax)/12 + monthly_income[n]*capex/100 + monthly_income[n]*vacancy/100 + monthly_income[n]*repairs_maintain/100 + monthly_income[n]*management_fee/100)*(1+(expense_growth/100)))
        monthly_profit.append(monthly_income[n] - monthly_expenses[n])
        equity_in_property.append(prop_val[n] + monthly_profit[n] - end_bal[n])
    else:
        payment_number.append(n)
        pay.append(float(
            inital_loan_amount * monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** (-1 * loan_length * 12))))
        loan_beg_bal.append(float(end_bal[n-1]))
        interest_to_pay.append(float(loan_beg_bal[n] * monthly_interest_rate))
        principal.append(pay[n] - interest_to_pay[n])
        end_bal.append(loan_beg_bal[n] - principal[n])
        prop_val.append(prop_val[n-1]*(1+(capital_gain/100/12)))
        monthly_income.append(monthly_income[n-1]*(1+(rental_growth/100/12)))
        monthly_expenses.append((monthly_expenses[n-1])*(1+(expense_growth/1200)))
        monthly_profit.append(monthly_income[n]-monthly_expenses[n])
        equity_in_property.append(equity_in_property[n-1] + monthly_profit[n] + (prop_val[n]-prop_val[n-1]))

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

#     'Beginning Balance of Loan': loan_beg_bal,
#     'Payment': pay,
#     'Interest': interest_to_pay,
#     'Principal': principal,
#     'Ending Balance': end_bal,
#     'Property Value': prop_val,
#     'Monthly Income': monthly_income,
#     'Monthly Expenses': monthly_expenses,
#     'Monthly Profit': monthly_profit,
#     'Equity in Property': equity_in_property,
# }))


#


# Print specified input parameters
# st.write(df)
# st.write('---')
#


