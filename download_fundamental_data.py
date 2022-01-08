'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang
@Date          : June 2021

@Student Name  : Fei Zhai

https://github.com/JECSand/yahoofinancials

'''

import pandas as pd
import csv

from utils import MyYahooFinancials as YF
import stock as stock_file


def read_ticker(input_file_name):
    df = pd.read_csv(input_file_name)
    return df['Symbol']

def process_single_ticker(ticker):
    tick = YF(ticker)
    ticker_info = pd.DataFrame({
                  'Symbol': ticker,
                  'Sector': tick.get_sector(ticker),
                  'EPS Next 5Y': "{percent:.2%}".format(percent = tick.get_eps_next_5y(ticker)),
                  'Market Cap': tick.get_market_cap(),
                  'Total Assets': tick.get_total_assets(),
                  'Total Debts': stock_file.Stock(ticker, 'annual').get_total_debt(),
                  'Free Cash Flow': stock_file.Stock(ticker, 'annual').get_free_cashflow(),
                  'Beta': tick.get_beta(),
                  'P/E Ratio': tick.get_pe_ratio(),
                  'Current Price': tick.get_current_price()
                  }, index=[0])
    df = pd.DataFrame(ticker_info)
    print(df)
    return df.values

def read_header(input_file_name):
    df = pd.read_csv(input_file_name)
    return df.columns

def append_result(result, input_file_name, output_file_name):
    with open(output_file_name, 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(result)

def download_fundamental_data(input_file_name, output_file_name):
    headers = read_header(input_file_name)
    with open(output_file_name, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)

    tickers = read_ticker(input_file_name)    
    for ticker in tickers:
        result = process_single_ticker(ticker)
        append_result(result, input_file_name, output_file_name)

def run():
    input_fname = "./StockUniverse.csv"
    output_fname = "./StockUniverseWithData.csv"
    
    download_fundamental_data(input_fname, output_fname)
    
if __name__ == "__main__":
    run()
