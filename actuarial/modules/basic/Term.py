import math
import pandas as pd
from actuarial.functions.basic_func import alpha, beta
from database import DBconn
''' Notation '''
# x: age    # omega: age end    # i: interest rate

''' File Settings '''
mortTable = DBconn.getLifeTable()

class Term():
    def __init__(self, x, gender, n, m=None, omega=105, i=0.02):
        self.x = x
        self.gender = gender
        self.m = m
        self.n = n
        self.omega = omega
        self.i = i
        self.i_m = m * ((1 + i) ** (1 / m) - 1) if m else None
        self.delta = math.log(1 + i)

        index = (mortTable["Gender"] == gender) & (mortTable["Age"] == x - 1) if x > 0 else 1
        p_1 = mortTable[index]["MortRate"].tolist()[0]
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] == x)
        p_2 = mortTable[index]["MortRate"].tolist()[0]
        self.mu_x = -(math.log(p_1) + math.log(p_2)) / 2

        index = (mortTable["Gender"] ==self.gender) & (mortTable["Age"] == x + self.n - 1) if x + n > 0 else 1
        p_1 = mortTable[index]["MortRate"].tolist()[0]
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] == x + n)
        p_2 = mortTable[index]["MortRate"].tolist()[0]
        self.mu_xn = -(math.log(p_1) + math.log(p_2)) / 2

    def change(self, target, value):
        if target == 'x':
            self.x = value
        elif target == 'gender':
            self.gender = value
        elif target == 'm':
            self.m = value
            self.i_m = value * ((1 + self.i) ** (1 / value) - 1) if value else None
        elif target == 'n':
            self.n = value
        elif target == 'omega':
            self.omega = value
        elif target == 'i':
            self.i = value
            self.i_m = self.m * ((1 + value) ** (1 / self.m) - 1) if self.m else None
            self.delta = math.log(1 + value)
        index = (mortTable["Gender"] == self.gender) & (mortTable["Age"] == self.x - 1) if self.x > 0 else 1
        p_1 = mortTable[index]["MortRate"].tolist()[0]
        index = (mortTable["Gender"] == self.gender) & (mortTable["Age"] == self.x)
        p_2 = mortTable[index]["MortRate"].tolist()[0]
        self.mu_x = -(math.log(p_1) + math.log(p_2)) / 2

        index = (mortTable["Gender"] == self.gender) & (mortTable["Age"] == self.x + self.n - 1) if self.x + self.n > 0 else 1
        p_1 = mortTable[index]["MortRate"].tolist()[0]
        index = (mortTable["Gender"] == self.gender) & (mortTable["Age"] == self.x + self.n)
        p_2 = mortTable[index]["MortRate"].tolist()[0]
        self.mu_xn = -(math.log(p_1) + math.log(p_2)) / 2

    ''' Term A Funcs '''
    # continuous case
    def A_bar_1_x_n(self, method=0):
        # UDD assumption
        if method == 0:
            return self.A_1_x_n() * self.i / self.delta
        # Claims acceleration approach
        elif method == 1:
            return self.A_1_x_n() * (1 + self.i) ** 0.5

    # annual case
    def A_1_x_n(self):
        survivals = 1
        A = 0
        discount = (1 + self.i) ** -1
        years = min(self.n, self.omega - self.x)
        for year in range(years):
            index = (mortTable["Gender"] == self.gender) & (mortTable["Age"] == self.x + year)
            mort_rate = mortTable[index]["MortRate"].tolist()[0] if year < years - 1 else 1
            deaths = survivals * mort_rate
            A += deaths * discount
            survivals -= deaths
            discount /= (1 + self.i)
        return A

    # Term Life Insurance, 1/mthly case
    def A_m_1_x_n(self, method=0):
        # UDD assumption
        if method == 0:
            return self.A_1_x_n() * self.i / self.i_m
        # Claims acceleration approach
        elif method == 1:
            return self.A_1_x_n() * (1 + self.i) ** ((self.m - 1) / (2 * self.m))

    ''' Term a Funcs '''
    # due n case
    def a_due_x_n(self):
        survivals = 1
        a = 0
        discount = 1
        years = min(self.n, self.omega - self.x)
        for year in range(years):
            a += survivals * discount
            index = (mortTable["Gender"] == self.gender) & (mortTable["Age"] == self.x + year)
            mort_rate = mortTable[index]["MortRate"].tolist()[0] if year < years - 1 else 1
            survivals *= (1 - mort_rate)
            discount /= (1 + self.i)
        return a

    # immediate n case
    def a_imm_x_n(self):
        survivals = 1
        a = 0
        discount = 1
        years = min(self.omega - self.x, self.n)
        for year in range(1, years + 1):
            a += survivals * discount
            index = (mortTable["Gender"] == self.gender) & (mortTable["Age"] == self.x + year)
            mort_rate = mortTable[index]["MortRate"].tolist()[0] if year < years else 1
            survivals *= (1 - mort_rate)
            discount /= (1 + self.i)
        return a

    # due 1/mthly n case
    def a_due_m_x_n(self, method=0):
        years = min(self.omega - self.x, self.n)
        p_n = 1
        for year in range(years):
            index = (mortTable["Gender"] == self.gender) & (mortTable["Age"] == self.x + year)
            mort_rate = mortTable[index]["MortRate"].tolist()[0]
            p_n *= (1 - mort_rate)

        # UDD assumption
        if method == 0:
            return alpha(self.m, i=self.i) * self.a_due_x_n() - beta(self.m, i=self.i) * (1 - self.v ** self.n * p_n)
        # Woolhouse's formula
        elif method == 1:
            return self.a_due_x_n() - (1 - self.v ** self.n * p_n) * (self.m - 1) / (2 * self.m) - (self.delta + self.mu_x - self.v ** self.n * p_n * (self.delta + self.mu_xn)) * (self.m ** 2 - 1) / (12 * self.m ** 2)

    # due continuous n case
    def a_conti_x_n(self, method=0):
        p_n = 1
        for year in range(min(self.omega - self.x, self.n)):
            index = (mortTable["Gender"] == self.gender) & (mortTable["Age"] == self.x + year)
            mort_rate = mortTable[index]["MortRate"].tolist()[0]
            p_n *= (1 - mort_rate)

        # UDD assumption
        if method == 0:
            return self.i * self.d * self.a_due_x_n() / (self.delta ** 2) - (self.i - self.delta) * (1 - self.v ** self.n * p_n) / (self.delta ** 2)
        # Woolhouse's formula
        elif method == 1:
            return self.a_due_x_n() - (1 - self.v ** self.n * p_n) / 2 - (self.delta + self.mu_x - self.v ** self.n * p_n * (self.delta + self.mu_xn)) / 12