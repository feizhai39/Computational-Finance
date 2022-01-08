'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang

@Student Name  : Fei Zhai

@Date          : June 2021


'''
import enum
import calendar
import math
import pandas as pd
import numpy as np

import datetime 
from scipy.stats import norm
from download_fundamental_data import *

from math import log, exp, sqrt

from utils import MyYahooFinancials

class Stock(object):
    '''
    Stock class for getting financial statements as well as pricing data
    '''
    def __init__(self, symbol, freq):
        self.symbol = symbol
        self.yfinancial = MyYahooFinancials(symbol, freq)
        self.ohlcv_df = None
     
    
    def __init__(self, symbol, spot_price = None, sigma = None, dividend_yield = 0, freq = 'annual'):
        self.symbol = symbol
        self.spot_price = spot_price
        self.sigma = sigma
        self.dividend_yield = dividend_yield
        self.yfinancial = MyYahooFinancials(symbol, freq)
        self.ohlcv_df = None
        

    def get_daily_hist_price(self, start_date, end_date):
        '''
        Get historical OHLCV pricing dataframe
        '''
        #TODO
        self.ohlcv_df = self.yfinancial.get_historical_price_data(start_date, end_date, 'daily')
        pricing_df = pd.DataFrame(self.ohlcv_df[self.symbol]['prices'])
        pricing_df = pricing_df.drop('date', axis=1).set_index('formatted_date')
        
        return(pricing_df)
        #end TODO
        
    def calc_returns(self):
        '''
        '''
        self.ohlcv_df['prev_close'] = self.ohlcv_df['close'].shift(1)
        self.ohlcv_df['returns'] = (self.ohlcv_df['close'] - self.ohlcv_df['prev_close'])/ \
                                        self.ohlcv_df['prev_close']


    # financial statements related methods
    
    def get_total_debt(self):
        '''
        compute total_debt as long term debt + current debt 
        current debt = total current liabilities - accounts payables - other current liabilities (ignoring current deferred liabilities)
        '''
        result = None
        # TODO
        try:
            current_debt = self.yfinancial.get_total_current_liabilities() - self.yfinancial.get_account_payable() - self.yfinancial.get_other_current_liabilities()
            result = self.yfinancial.get_long_term_debt() + current_debt
            return(result)
        except Exception:
        # end TODO
            return(result)

    def get_free_cashflow(self):
        '''
        get free cash flow as operating cashflow + capital expenditures (which will be negative)
        ''' 
        result = None
        # TODO
        try:
            result = self.yfinancial.get_operating_cashflow() + self.yfinancial.get_capital_expenditures()
            return(result)
        except Exception:
        # end TODO
            return(result)

    def get_cash_and_cash_equivalent(self):
        '''
        Return cash plus short term investment 
        '''
        result = None
        # TODO
        result = self.yfinancial.get_cash() + self.yfinancial.get_short_term_investments()
        # end TODO
        return(result)

    def get_num_shares_outstanding(self):
        '''
        get current number of shares outstanding from Yahoo financial library
        '''
        result = None
        # TODO
        result = self.yfinancial.get_num_shares_outstanding()
        # end TODO
        return(result)

    def get_beta(self):
        '''
        get beta from Yahoo financial
        '''
        result = None
        # TODO
        result = self.yfinancial.get_beta()
        # end TODO
        return(result)

    def lookup_wacc_by_beta(self):
        '''
        lookup wacc by using the table in Slide 15 of the DiscountedCashFlowModel lecture powerpoint
        '''
        result = None
        # TODO:
        beta = self.get_beta()
        
        if beta < 0.8:
            result = 0.05
        elif beta < 1.0:
            result = 0.06
        elif beta < 1.1:
            result = 0.065
        elif beta < 1.2:
            result = 0.07
        elif beta < 1.3:
            result = 0.075
        elif beta < 1.5:
            result = 0.08
        elif beta < 1.6:
            result = 0.085
        elif beta >= 1.6:
            result = 0.09
        #end TODO
        return(result)
        
def _test():
    symbol = 'AAPL'
    from_date = datetime.date(2021, 6, 1).strftime("%Y-%m-%d")
    end_date = datetime.date(2021, 6, 26).strftime("%Y-%m-%d")

    stock = Stock(symbol, 'annual')
    print("Ticker:", symbol)
    print("Total Debt:", stock.get_total_debt())
    print("Beta:", stock.get_beta())
    print("WACC:", stock.lookup_wacc_by_beta())
    print("Free Cashflow:", stock.get_free_cashflow())
    print("Cash Equivalent:", stock.get_cash_and_cash_equivalent())
    print("Outstanding Shares:", stock.get_num_shares_outstanding())
    print(stock.get_daily_hist_price(from_date, end_date))



if __name__ == "__main__":
    _test()
