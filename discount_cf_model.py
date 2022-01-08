'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang

@Student Name  : To the Moon

@Date          : June 2021

Discounted Cash Flow Model with Financial Data from Yahoo Financial

https://medium.datadriveninvestor.com/how-to-calculate-intrinsic-value-of-a-stock-aapl-case-study-935fb062004b

'''
import enum
import calendar
import math
import pandas as pd
import numpy as np

import datetime 
from scipy.stats import norm

from math import log, exp, sqrt
from stock import *

class DiscountedCashFlowModel(object):
    '''
    DCF Model:

    FCC is assumed to go have growth rate by 3 periods, each of which has different growth rate
           short_term_growth_rate for the next 5Y
           medium_term_growth_rate from 6Y to 10Y
           long_term_growth_rate from 11Y to 20thY
    '''

    def __init__(self, stock, as_of_date):
        self.stock = stock
        self.as_of_date = as_of_date

        self.short_term_growth_rate = None
        self.medium_term_growth_rate = None
        self.long_term_growth_rate = None


    def set_FCC_growth_rate(self, short_term_rate, medium_term_rate, long_term_rate):
        self.short_term_growth_rate = short_term_rate
        self.medium_term_growth_rate = medium_term_rate
        self.long_term_growth_rate = long_term_rate


    def calc_fair_value(self):
        '''
        calculate the fair_value using DCF model

        1. calculate a yearly discount factor using the WACC
        2. Get the Free Cash flow
        3. Sum the discounted value of the FCC for the first 5 years using the short term growth rate
        4. Add the discounted value of the FCC from year 6 to the 10th year using the medium term growth rate
        5. Add the discounted value of the FCC from year 10 to the 20th year using the long term growth rate
        6. Compute the PV as cash + short term investments - total debt + the above sum of discounted free cash flow
        7. Return the stock fair value as PV divided by num of shares outstanding

        '''
        DCF = 0
        WACC = self.stock.lookup_wacc_by_beta()
        DF = 1/(1+ WACC)
        FCC = self.stock.get_free_cashflow()
        EPS5Y = self.short_term_growth_rate
        EPS6To10Y = self.medium_term_growth_rate
        EPS10To20Y = self.long_term_growth_rate
    
        for i in range(1, 6):
            DCF += FCC * (1+ EPS5Y)**i * DF ** i
    
        CF5 = FCC * (1+EPS5Y)**5
        for i in range(1, 6):
            DCF += CF5 * (1+EPS6To10Y)**i * DF ** (i+5)
    
        CF10 = CF5 * (1+EPS6To10Y)**5
        for i in range(1, 11):
            DCF += CF10 * (1+EPS10To20Y)**i * DF **(i + 10)
            
             
        current_cash = self.stock.get_cash_and_cash_equivalent()
        total_debt = self.stock.get_total_debt()
        PV = current_cash - total_debt + DCF
        
        
        #fair value
        num_shares = self.stock.get_num_shares_outstanding()
        result = PV/num_shares
    
        return(result)


def _test():
    symbol = 'AAPL'
    as_of_date = datetime.date(2021, 6, 26)

    stock = Stock(symbol, 'annual')
    model = DiscountedCashFlowModel(stock, as_of_date)
    
    print("Symbol:", symbol)
    print("Shares:", stock.get_num_shares_outstanding())
    print("FCC:", stock.get_free_cashflow())
    print("Beta:", stock.get_beta())
    print("WACC:", stock.lookup_wacc_by_beta())
    print("Total Debt:", stock.get_total_debt())
    print("Cash and Cash Equivalent:", stock.get_cash_and_cash_equivalent())

    # look up from Finviz
    eps5y = 0.1793
    model.set_FCC_growth_rate(eps5y, eps5y/2, 0.04)

    model_price = model.calc_fair_value()
    print("Fair Value:", model_price)

if __name__ == "__main__":
    _test()
