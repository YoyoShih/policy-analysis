from functools import reduce
import math
from numpy import logspace, concatenate
from pandas import read_csv

''' Notation '''
# x: age    # omega: age end    # i: interest rate

''' Constant '''
AGE_END = 110
root_path = 'D:/Desktop/Actuarial Side Project/Policy Analysis/docs'
mortTable = read_csv(f'{root_path}/2021TSO.csv')

# Whole Life Insurance Functions
''' Whole Life Insurance, continuous case '''
def A_bar_x(x, gender, omega=105, i=0.02, method=0):
    # UDD assumption
    if method == 0:
        delta = math.log(1+i)
        return A_x(x, gender, omega=omega, i=i) * i / delta
    # Claims acceleration approach
    elif method == 1:
        return A_x(x, gender, omega=omega, i=i) * (1 + i) ** 0.5

''' Whole Life Insurance, annual case '''
def A_x(x, gender, omega=105, i=0.02):
    years = omega-x if omega != AGE_END else omega-x+1
    discounts = logspace(-1, -years, num=years, base=1+i)
    index = (mortTable["Gender"] == gender) & (mortTable["Age"] >= x) & (mortTable["Age"] < x+years)
    mort_rates = mortTable[index]["MortRate"].to_numpy()
    survivals_rate = concatenate(([1], (lambda x: 1-x)(mort_rates)[:-1]))
    survivals = survivals_rate.cumprod()
    return sum(discounts*survivals*mort_rates)

''' Whole Life Insurance, 1/mthly case '''
def A_m_x(x, gender, m, omega=105, i=0.02, method=0):
    # UDD assumption
    if method == 0:
        i_m = m * ((1 + i) ** (1 / m) - 1)
        return A_x(x, gender, omega=omega, i=i) * i / i_m
    # Claims acceleration approach
    elif method == 1:
        return A_x(x, gender, omega=omega, i=i) * (1 + i) ** ((m - 1) / (2 * m))

# Term Insurance Functions
''' Term Life Insurance, continuous case '''
def A_bar_1_x_n(x, gender, n, omega=105, i=0.02, method=0):
    # UDD assumption
    if method == 0:
        delta = math.log(1 + i)
        return A_1_x_n(x, gender, n, omega=omega, i=i) * i / delta
    # Claims acceleration approach
    elif method == 1:
        return A_1_x_n(x, gender, n, omega=omega, i=i) * (1 + i) ** 0.5

''' Term Life Insurance, annual case '''
def A_1_x_n(x, gender, n, omega=105, i=0.02):
    years = min(n, omega - x if omega != AGE_END else omega - x + 1)
    discounts = logspace(-1, -years, num=years, base=1+i)
    index = (mortTable["Gender"] == gender) & (mortTable["Age"] >= x) & (mortTable["Age"] < x+years)
    mort_rates = mortTable[index]["MortRate"].to_numpy()
    survivals_rate = concatenate(([1], (lambda x: 1-x)(mort_rates)[:-1]))
    survivals = survivals_rate.cumprod()
    return sum(discounts*survivals*mort_rates)

''' Term Life Insurance, 1/mthly case '''
def A_m_1_x_n(x, gender, m, n, omega=105, i=0.02, method=0):
    # UDD assumption
    if method == 0:
        i_m = m * ((1 + i) ** (1 / m) - 1)
        return A_1_x_n(x, gender, n, omega=omega, i=i) * i / i_m
    # Claims acceleration approach
    elif method == 1:
        return A_1_x_n(x, gender, n, omega=omega, i=i) * (1 + i) ** ((m - 1) / (2 * m))

# Endowment Insurance Functions
''' Pure Endowment '''
def nEx(x, gender, n, omega=105, i=0.02, t=0):
    years = min(n, omega-x if omega != AGE_END else omega-x+1)-t
    index = (mortTable["Gender"] == gender) & (mortTable["Age"] >= x+t) & (mortTable["Age"] < x+t+years)
    mort_rates = mortTable[index]["MortRate"].to_list()
    survivals = reduce(lambda x,y: x*(1-y), [1]+mort_rates)
    return survivals / (1 + i) ** years

''' Endowment Insurance, continuous case '''
def A_bar_x_n(x, gender, n, omega=105, i=0.02, method=0):
    return A_bar_1_x_n(x, gender, n, omega=omega, i=i, method=method) + nEx(x, gender, n, omega=omega, i=i)

''' Endowment Insurance, annual case '''
def A_x_n(x, gender, n, omega=105, i=0.02):
    return A_1_x_n(x, gender, n, omega=omega, i=i) + nEx(x, gender, n, omega=omega, i=i)

''' Endowment Insurance, 1/mthly case '''
def A_m_x_n(x, gender, m, n, omega=105, i=0.02, method=0):
    return A_m_1_x_n(x, gender, m, n, omega=omega, i=i, method=method) + nEx(x, gender, n, omega=omega, i=i)