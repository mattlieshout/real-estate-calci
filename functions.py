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
from calc_display import *



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
    st.write(property_address)
    c.execute('DELETE FROM blogtable WHERE property_address="{}"'.format(property_address))
    conn.commit()
#