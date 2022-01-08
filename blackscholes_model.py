'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang

@Student Name  : To the Moon

@Date          : June 2021


'''

import datetime
from scipy.stats import norm
from math import log, exp, sqrt

from stock import Stock
from option import *

class BlackScholesModel(object):
    '''
    OptionPricer
    '''

    def __init__(self, pricing_date, risk_free_rate):
        self.pricing_date = pricing_date
        self.risk_free_rate = risk_free_rate

    def calc_parity_price(self, option, option_price):
        '''
        return the put price from Put-Call Parity if input option is a call
        else return the call price from Put-Call Parity if input option is a put
        '''
        result = None
        # TODO: implement details here
        if option.option_type == Option.Type.CALL:
            result = option_price + option.strike *exp(-self.risk_free_rate * option.time_to_expiry)-option.underlying.spot_price*exp(-option.underlying.dividend_yield * option.time_to_expiry)
          
        else:
            result = option_price +option.underlying.spot_price*exp(-option.underlying.dividend_yield * option.time_to_expiry)-option.strike *exp(-self.risk_free_rate * option.time_to_expiry)
            
        # end TODO
        return(result)

    def calc_model_price(self, option):
        '''
        Calculate the price of the option using Black-Scholes model
        '''
        px = None
        if option.option_style == Option.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == Option.Style.EUROPEAN:
            
            S0 = option.underlying.spot_price
            sigma = option.underlying.sigma
            T = option.time_to_expiry
            K = option.strike
            q = option.underlying.dividend_yield
            r = self.risk_free_rate

            d1 = (log(S0/K)+(r-q+pow(sigma,2)/2)*T)/(sigma * sqrt(T))
            d2 = d1 - sigma*sqrt(T)
            if option.option_type == Option.Type.CALL:
                px = S0*exp(-q*T)*norm.cdf(d1)-K*exp(-r*T)*norm.cdf(d2)
            else:
                px = K*exp(-r*T)*norm.cdf(-d2)-S0*exp(-q*T)*norm.cdf(-d1) 
        else:
            raise Exception("Unsupported option type")        
        return(px)

    def calc_delta(self, option):
        if option.option_style == Option.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == Option.Style.EUROPEAN:
            S0 = option.underlying.spot_price
            sigma = option.underlying.sigma
            T = option.time_to_expiry
            K = option.strike
            q = option.underlying.dividend_yield
            r = self.risk_free_rate
            # TODO:
            if S0/K == 0: 
                return 0
            d1 = (log(S0/K)+(r-q+pow(sigma,2)/2)*T)/(sigma * sqrt(T))
            if option.option_type == Option.Type.CALL:
                result = exp(-q**T)*norm.cdf(d1)
            else:
                result = exp(-q**T)*(norm.cdf(d1)-1)
            # end TODO
        else:
            raise Exception("Unsupported option type")

        return result

    def calc_gamma(self, option):

        if option.option_style == Option.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == Option.Style.EUROPEAN:
            # TODO:
            result = None
            S0 = option.underlying.spot_price
            sigma = option.underlying.sigma
            T = option.time_to_expiry
            K = option.strike
            q = option.underlying.dividend_yield
            r = self.risk_free_rate
            if S0/K == 0: 
                return 0
            d1 = (log(S0/K)+(r-q+pow(sigma,2)/2)*T)/(sigma * sqrt(T))
            result = (norm.pdf(d1) *exp(-q*T))/(S0*sigma * sqrt(T))

            # end TODO
        else:
            raise Exception("Unsupported option type")

        return result

    def calc_theta(self, option):
        if option.option_style == Option.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == Option.Style.EUROPEAN:
            result = None
            S0 = option.underlying.spot_price
            sigma = option.underlying.sigma
            T = option.time_to_expiry
            K = option.strike
            q = option.underlying.dividend_yield
            r = self.risk_free_rate
            if S0/K == 0: 
                return 0
            d1 = (log(S0/K)+(r-q+pow(sigma,2)/2)*T)/(sigma * sqrt(T))
            d2 = d1 - sigma*sqrt(T)
            if option.option_type == Option.Type.CALL:
                result = ((-S0 *norm.pdf(d1) *sigma*exp(-q*T))/(2*sqrt(T)))+q*S0*norm.cdf(d1)*exp(-q*T)-r*K*exp(-r*T)*norm.cdf(d2)
            else:
                result = ((-S0 *norm.pdf(d1) *sigma*exp(-q*T))/(2*sqrt(T)))-q*S0*norm.cdf(-d1)*exp(-q*T)+r*K*exp(-r*T)*norm.cdf(-d2)
        else:
            raise Exception("Unsupported option type")

        return result

    def calc_vega(self, option):
        if option.option_style == Option.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == Option.Style.EUROPEAN:
            # TODO:
                result = None
                S0 = option.underlying.spot_price
                sigma = option.underlying.sigma
                T = option.time_to_expiry
                K = option.strike
                q = option.underlying.dividend_yield
                r = self.risk_free_rate
                if S0/K == 0: 
                    return 0
                d1 = (log(S0/K)+(r-q+pow(sigma,2)/2)*T)/(sigma * sqrt(T))
                #d2 = d1 - sigma*sqrt(T)
                result = S0*sqrt(T)*norm.pdf(d1)*exp(-q*T)
                # end TODO
        else:
            raise Exception("Unsupported option type")

        return result

    def calc_rho(self, option):
        if option.option_style == Option.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == Option.Style.EUROPEAN:          
            result = None
            S0 = option.underlying.spot_price
            sigma = option.underlying.sigma
            T = option.time_to_expiry
            K = option.strike
            q = option.underlying.dividend_yield
            r = self.risk_free_rate
            if S0/K == 0: 
                return 0
            d1 = (log(S0/K)+(r-q+pow(sigma,2)/2)*T)/(sigma * sqrt(T))
            d2 = d1 - sigma*sqrt(T)
            if option.option_type == Option.Type.CALL:
                result = K*T*exp(-r*T)*norm.cdf(d2)
            else:
                result = -K*T*exp(-r*T)*norm.cdf(-d2)
            # end TODO
        else:
            raise Exception("Unsupported option type")
        return result


def _test():

    symbol = 'AAPL'
    pricing_date = datetime.date(2021, 6, 1)

    risk_free_rate = 0.04
    model = BlackScholesModel(pricing_date, risk_free_rate)

    # .... use this as your unit test
    # calculate the B/S model price for a 3-month ATM call

    T = 3/12
    num_period = 2

    dt = T / num_period
    S0 = 130
    K = 130

    sigma = 0.3
    
    stock = Stock(symbol, S0, sigma)
    
    call = EuropeanCallOption(stock, T, K)
    
    model_price = model.calc_model_price(call)
    print(symbol, model_price)


if __name__ == "__main__":
    _test()
    
