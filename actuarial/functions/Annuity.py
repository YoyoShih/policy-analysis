from functools import reduce
import math
from numpy import logspace, concatenate
from actuarial.functions.basic_func import alpha, beta

''' Notation '''
# x: age    # omega: age end    # i: interest rate

''' Constant '''
AGE_END = 110
mortTable = None    # mortTable!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

''' Whole Life Annuity Functions '''
def a_due_x(x, gender, omega=105, i=0.02):
    years = omega-x if omega != AGE_END else omega-x+1
    discounts = logspace(0, -(years-1), num=years, base=1+i)
    index = (mortTable["Gender"] == gender) & (mortTable["Age"] >= x) & (mortTable["Age"] < x+years)
    mort_rates = mortTable[index]["MortRate"].to_numpy()
    survivals_rate = concatenate(([1], (lambda x: 1-x)(mort_rates)[:-1]))
    survivals = survivals_rate.cumprod()
    return sum(discounts*survivals)

def a_imm_x(x, gender, omega=105, i=0.02):
    years = omega-x if omega != AGE_END else omega-x+1
    discounts = logspace(-1, -years, num=years, base=1+i)
    index = (mortTable["Gender"] == gender) & (mortTable["Age"] >= x) & (mortTable["Age"] < x+years)
    mort_rates = mortTable[index]["MortRate"].to_numpy()
    survivals_rate = concatenate(([1], (lambda x: 1-x)(mort_rates)[:-1]))
    survivals = survivals_rate.cumprod()
    return sum(discounts*survivals)

def a_due_m_x(x, gender, m, omega=105, i=0.02, method=0):
    delta = math.log(1+i)
    # UDD assumption
    if method == 0:
        return alpha(m, i=i) * a_due_x(x, gender, omega=omega, i=i) - beta(m, i=i)
    # Woolhouse's formula
    else:
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] == x - 1) if x > 0 else 1
        p_1 = mortTable[index]["MortRate"].tolist()[0]
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] == x)
        p_2 = mortTable[index]["MortRate"].tolist()[0]
        mu_x = -(math.log(p_1) + math.log(p_2)) / 2
        return a_due_x(x, gender, omega=omega, i=i) - (m - 1) / (2 * m) - (delta + mu_x) * (m ** 2 - 1) / (12 * m ** 2)

def a_conti_x(x, gender, omega=105, i=0.02, method=0):
    v = 1 / (1 + i)
    d = 1 - v
    delta = math.log(1+i)
    # UDD assumption
    if method == 0:
        return i * d * a_due_x(x, gender, omega=omega, i=i) / (delta ** 2) - (i - delta) / (delta ** 2)
    # Woolhouse's formula
    else:
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] == x - 1) if x > 0 else 1
        p_1 = mortTable[index]["MortRate"].tolist()[0]
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] == x)
        p_2 = mortTable[index]["MortRate"].tolist()[0]
        mu_x = -(math.log(p_1) + math.log(p_2)) / 2
        return a_due_x(x, gender, omega=omega, i=i) - 0.5 - (delta + mu_x) / 12

''' Term Annuity Functions '''
def a_due_x_n(x, gender, n, omega=105, i=0.02):
    years = min(omega-x if omega != AGE_END else omega-x+1, n)
    discounts = logspace(0, -(years-1), num=years, base=1+i)
    index = (mortTable["Gender"] == gender) & (mortTable["Age"] >= x) & (mortTable["Age"] < x+years)
    mort_rates = mortTable[index]["MortRate"].to_numpy()
    survivals_rate = concatenate(([1], (lambda x: 1-x)(mort_rates)[:-1]))
    survivals = survivals_rate.cumprod()
    return sum(discounts*survivals)

def a_imm_x_n(x, gender, n, omega=105, i=0.02):
    years = min(omega-x if omega != AGE_END else omega-x+1, n)
    discounts = logspace(-1, -years, num=years, base=1+i)
    index = (mortTable["Gender"] == gender) & (mortTable["Age"] >= x) & (mortTable["Age"] < x+years)
    mort_rates = mortTable[index]["MortRate"].to_numpy()
    survivals_rate = concatenate(([1], (lambda x: 1-x)(mort_rates)[:-1]))
    survivals = survivals_rate.cumprod()
    return sum(discounts*survivals)

def a_due_m_x_n(x, gender, m, n, omega=105, i=0.02, method=0):
    v = 1 * (1 + i)
    delta = math.log(1 + i)
    years = min(omega-x if omega != AGE_END else omega-x+1, n)
    index = (mortTable["Gender"] == gender) & (mortTable["Age"] >= x) & (mortTable["Age"] < x+years)
    mort_rate = mortTable[index]["MortRate"].tolist()
    p_n = reduce(lambda x, y: x * (1-y), [1]+mort_rate)
    # UDD assumption
    if method == 0:
        return alpha(m, i=i) * a_due_x_n(x, gender, omega=omega, i=i) - beta(m, i=i) * (1 - v ** n * p_n)
    # Woolhouse's formula
    else:
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] == x-1) if x > 0 else 1
        p_1 = mortTable[index]["MortRate"].tolist()[0]
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] == x)
        p_2 = mortTable[index]["MortRate"].tolist()[0]
        mu_x = -(math.log(p_1) + math.log(p_2)) / 2
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] == x+n-1) if x + n > 0 else 1
        p_1 = mortTable[index]["MortRate"].tolist()[0]
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] == x+n)
        p_2 = mortTable[index]["MortRate"].tolist()[0]
        mu_xn = -(math.log(p_1) + math.log(p_2)) / 2
        return a_due_x_n(x, gender, omega=omega, i=i) - (1 - v ** n * p_n) * (m - 1) / (2 * m) - (delta + mu_x - v ** n * p_n * (delta + mu_xn)) * (m ** 2 - 1) / (12 * m ** 2)

def a_conti_x_n(x, gender, n, omega=105, i=0.02, method=0):
    v = 1 / (1 + i)
    d = 1 - v
    delta = math.log(1 + i)
    years = min(omega-x if omega != AGE_END else omega-x+1, n)
    index = (mortTable["Gender"] == gender) & (mortTable["Age"] >= x) & (mortTable["Age"] < x+years)
    mort_rate = mortTable[index]["MortRate"].tolist()
    p_n = reduce(lambda x, y: x * (1-y), [1]+mort_rate)
    # UDD assumption
    if method == 0:
        return i * d * a_due_x_n(x, gender, n, omega=omega, i=i) / (delta ** 2) - (i - delta) * (1 - v ** n * p_n) / (delta ** 2)
    # Woolhouse's formula
    else:
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] == x-1) if x > 0 else 1
        p_1 = mortTable[index]["MortRate"].tolist()[0]
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] == x)
        p_2 = mortTable[index]["MortRate"].tolist()[0]
        mu_x = -(math.log(p_1) + math.log(p_2)) / 2
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] == x+n-1) if x + n > 0 else 1
        p_1 = mortTable[index]["MortRate"].tolist()[0]
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] == x+n)
        p_2 = mortTable[index]["MortRate"].tolist()[0]
        mu_xn = -(math.log(p_1) + math.log(p_2)) / 2
        return a_due_x_n(x, gender, n, omega=omega, i=i) - (1 - v ** n * p_n) / 2 - (delta + mu_x - v ** n * p_n * (delta + mu_xn)) / 12
