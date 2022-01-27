import pandas as pd
from pandas import DataFrame
import numpy as np

import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from datetime import datetime
import pytz
import time

import re

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
browser = webdriver.Chrome(options=chrome_options)

def toNum(elementValue):
    onlyNumbers = ''
    for char in elementValue:
        if char.isnumeric() or char == '-' or char == '.' or char == '%':
            onlyNumbers += char

    # Divide percentages by 100 so they are valid floats
    if onlyNumbers[-1] == '%':
        return float(onlyNumbers[:-1]) / 100
    else:
        return float(onlyNumbers)

def currentESTTimestamp():
    utc_now = pytz.utc.localize(datetime.utcnow())
    est_now = utc_now.astimezone(pytz.timezone('America/New_York'))

    # SQL Format: 20120618 10:34:09 AM
    time_string = est_now.strftime('%Y%m%d %H:%M:%S %p')
    return time_string
    # time_string = time_string.replace('/', '')

browser.get('https://www.investing.com/currencies/streaming-forex-rates-majors')

fx_types = ['EUR/USD', 'USD/JPY', 'GBP/USD', 'USD/CHF', 'USD/CAD', 'AUD/USD','USD/INR','USD/CNY']

fx_ask_classnames = ['pid-1-ask', 'pid-3-ask', 'pid-2-ask', 'pid-4-ask',
                    'pid-7-ask', 'pid-5-ask', 'pid-160-ask', 'pid-2111-ask']

''' Create bid class names; same as fx_ask_classnames
    but has 'bid' at end of class name rather than 'ask' '''
fx_bid_classnames = []

for fx_ask_classname in fx_ask_classnames:
    curr_bid_classname = fx_ask_classname[:-3] + "bid"
    fx_bid_classnames.append(curr_bid_classname)

''' Create percentage class names; same as fx_ask_classnames
    but has 'pcp' at end of class name rather than 'ask' '''
fx_perc_classnames = []

for fx_ask_classname in fx_ask_classnames:
    curr_perc_classname = fx_ask_classname[:-3] + "pcp"
    fx_perc_classnames.append(curr_perc_classname)

    #------------------------------------------------------------------------------------------------------

    ''' !! To store dictionaries with type, classname, and current rate (once scraped) !! '''
    fx_rates_data = []

    for x in range(len(fx_ask_classnames)):
        curr_fx_rate_dic = {}
        curr_ask = toNum(browser.find_element_by_class_name(fx_ask_classnames[x]).text)
        curr_bid = toNum(browser.find_element_by_class_name(fx_bid_classnames[x]).text)
        # curr_ask_perc = toNum(browser.find_element_by_class_name(fx_perc_classnames[x]).text)

        # Fill dictionary with relevant info (type name, class name, ask, and reciprocal ask)
        curr_fx_rate_dic['fx_type_name'] = fx_types[x]
        curr_fx_rate_dic['fx_class_name'] = fx_ask_classnames[x]
        curr_fx_rate_dic['fx_ask'] = curr_ask
        # curr_fx_rate_dic['fx_bid'] = curr_bid
        curr_fx_rate_dic['fx_ask_reciprocal'] = np.reciprocal(curr_ask).item()
        curr_fx_rate_dic['fx_bid_reciprocal'] = np.reciprocal(curr_bid).item()
        # curr_fx_rate_dic['fx_ask_perc_change'] = curr_ask_perc
        # curr_fx_rate_dic['fx_is_positive'] = 1 if curr_ask_perc >= 0 else 0

        ''' Format for creating datetime obj:
            insert into table1(approvaldate)values('20120618 10:34:09 AM');
            !! TAKEN CARE OF IN currentESTTimestamp() !!
            (from https://stackoverflow.com/questions/12957635/sql-query-to-insert-datetime-in-sql-server) '''
        curr_fx_rate_dic['time_fetched'] = currentESTTimestamp()

        fx_rates_data.append(curr_fx_rate_dic)

    for data in fx_rates_data:
        print(data)



























































# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as ec
# from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager

# chrome_options = Options()
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--incognito")
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_experimental_option("prefs", { 
#     "profile.default_content_setting_values.notifications": 2,
#     "profile.default_content_settings.cookies": 2,
# })


# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# caps = DesiredCapabilities().CHROME
# caps["pageLoadStrategy"] = "none" 

