'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang
@Date          : June 2021

@Student Name  : Fei Zhai

https://github.com/JECSand/yahoofinancials

'''

from yahoofinancials import YahooFinancials 
import pandas as pd
import csv

class MyYahooFinancials(YahooFinancials):
    '''
    Extended class based on YahooFinancial libary

    '''
    def __init__(self, symbol, freq = 'annual'):
        YahooFinancials.__init__(self, symbol)
        self.freq = freq

    def get_operating_cashflow(self):
        try:
            return self._financial_statement_data('cash', 'cashflowStatementHistory', 'totalCashFromOperatingActivities', self.freq)
        except Exception:
            return None

    def get_capital_expenditures(self):
        try:
            return self._financial_statement_data('cash', 'cashflowStatementHistory', 'capitalExpenditures', self.freq)
        except Exception:
            return None

    def get_long_term_debt(self):
        try:
            return self._financial_statement_data('balance', 'balanceSheetHistory', 'longTermDebt', self.freq)
        except Exception:
            return None    

    def get_account_payable(self):
        try:
             return self._financial_statement_data('balance', 'balanceSheetHistory', 'accountsPayable', self.freq)
        except Exception:
            return None

    def get_total_current_liabilities(self):
        try:
            return self._financial_statement_data('balance', 'balanceSheetHistory', 'totalCurrentLiabilities', self.freq)
        except Exception:
            return None

    def get_other_current_liabilities(self):
        try:
            return self._financial_statement_data('balance', 'balanceSheetHistory', 'otherCurrentLiab', self.freq)
        except Exception:
            return None

    def get_cash(self):
        try:
            return self._financial_statement_data('balance', 'balanceSheetHistory', 'cash', self.freq)
        except Exception:
            return None

    def get_short_term_investments(self):
        try:
            return self._financial_statement_data('balance', 'balanceSheetHistory', 'shortTermInvestments', self.freq)
        except Exception:
            return None
    
    def get_total_assets(self):
        try:
            return self._financial_statement_data('balance', 'balanceSheetHistory', 'totalAssets', self.freq)
        except Exception:
            return None
        
    def get_sector(self, symbol):
        try:
            input_fname = "./StockUniverse.csv"
            df = pd.read_csv(input_fname)
            for i in df.index:
                ticker = df['Symbol'].iloc[i]
                if symbol == ticker: 
                    return df.at[i, 'Sector']
        except Exception:
            return None
        
    def get_eps_next_5y(self, symbol):
        try:
            input_fname = "./StockUniverse.csv"
            df = pd.read_csv(input_fname)
            for i in df.index:
                ticker = df['Symbol'].iloc[i]
                if symbol == ticker: 
                    return df.at[i, 'EPS Next 5Y']
        except Exception:
            return None

def _test():
    symbol = 'AAPL'
    
    yfinance = MyYahooFinancials(symbol)

    
    print("Getting Financial Data for {}".format(symbol))
    print("Long Term Debt: ", yfinance.get_long_term_debt())


if __name__ == "__main__":
    _test()
