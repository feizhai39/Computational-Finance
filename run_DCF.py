'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang
@Date          : June 2021

@Student Name  : Fei Zhai

'''

import pandas as pd
import datetime

from stock import Stock
from discount_cf_model import DiscountedCashFlowModel
from download_fundamental_data import *

def run():
    input_fname = "StockUniverse.csv"
    output_fname = "StockUniverseValuation.csv"

    as_of_date = datetime.date(2021, 6, 26)
    df = pd.read_csv(input_fname)
    
    # TODO
    header_names = ['Symbol', 'Fair Value']
    with open(output_fname, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header_names)
        
    for row in df.index:
        try:
            stock = Stock(df['Symbol'].iloc[row], 'annual')
            model = DiscountedCashFlowModel(stock, as_of_date)

            short_term_growth_rate = float(df.at[row, 'EPS Next 5Y'])
            medium_term_growth_rate = short_term_growth_rate/2
            long_term_growth_rate = 0.04

            model.set_FCC_growth_rate(short_term_growth_rate, medium_term_growth_rate, long_term_growth_rate)
            fair_value = model.calc_fair_value()
            results = pd.DataFrame({
                                    'Symbol': stock.symbol,
                                    'Fair Value': fair_value
                                    }, index=[0])
            with open(output_fname, 'a') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerows(results.values)
                
            print("Symbol:", stock.symbol)
            print("Fair Value:", fair_value)
            
        except Exception:
            fair_value = None
            results = pd.DataFrame({
                                    'Symbol': stock.symbol,
                                    'Fair Value': None
                                    }, index=[0])
            with open(output_fname, 'a') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerows(results.values)
            
            print("Symbol:", stock.symbol)
            print("Fair Value:", fair_value)
    
    # end TODO

    
if __name__ == "__main__":
    run()
