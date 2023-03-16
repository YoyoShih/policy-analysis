from dataclasses import dataclass, field
from pandas import read_csv, DataFrame, concat
from numpy import logspace, concatenate
from actuarial.modules.KC1KC2.pricing import Pricing
from database import DBconn

''' Notation '''
# x: age    # omega: age end    # i: interest rate  # S: sum assured    PPP: Premiums Payment Period   
# multiple: benefit multiple in preperiod   # pre-period: period that benefit equal premium * multiple

# purpose: 0 -> pricing, 1 -> reserve

''' File Settings '''
root_path = 'C:/Users/shih/ActuaViz/docs/'
mortTable = DBconn.getLifeTable()
GPTable = read_csv(f'{root_path}Insur Info/GP.csv')

@dataclass
class Reserve:
    x: int
    gender: int
    discount_rate: float = 0
    S: int = 10000
    PPP: int= 20
    pre_period: int = 3
    omega: int = 105
    multiple: float = 1.025
    life: int = field(init=False)
    VX_law: list = field(init=False)
    VDs: list = field(init=False)
    result: DataFrame = field(init=False)

    def __post_init__(self):
        self.life = self.omega - self.x
        x, gender = self.x, self.gender
        self.pricing = Pricing(x, gender, 0.02, purpose=0)
        self.reserve = Pricing(x, gender, 0.01, purpose=1)
        self.__VX_Law()
        self.__VD()
        self.__Result(x, gender, 0.01)

    ''' By Law '''
    def __VX_Law(self):
        p_result, r_result = self.pricing.result, self.reserve.result
        VL, VX = p_result['VL'], r_result['VX']
        VX_law = []
        years = self.life + 1
        for i in range(years):
            VX_law.append(max(VL[i], VX[i]))
        self.VX_law = VX_law
        return self.VX_law

    ''' Value of Deficiency Reserve '''
    def __VD(self):
        discount_rate = self.discount_rate
        GP = self.pricing.premium['GP']
        alter_NPs = self.reserve.premium['alter NPs']
        VDs = []
        years = min(self.life, self.PPP)
        for i in range(years):
            VDs.append(max(0, alter_NPs[i] - GP * (1 - discount_rate)))
        self.VDs = VDs
        return VDs

    def __VDPV(self, x, gender, i, t=0):
        VDs = self.VDs[t:]
        years = max(0, min(self.reserve.life, self.reserve.PPP) - t)
        discounts = logspace(0, -(years-1), num=years, base=1+i)
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] >= x+t) & (mortTable["Age"] < x+t+years)
        mort_rates = mortTable[index]["MortRate"].to_numpy()
        survivals_rate = concatenate(([1], (lambda x: 1-x)(mort_rates)[:-1]))
        survivals = survivals_rate.cumprod()
        return sum(VDs*survivals*discounts)

    ''' Result '''
    def __Result(self, x, gender, i):
        cols = ['t', 'VX Law', 'VDs', 'VD PV']
        result = DataFrame(columns=cols)
        years = self.life + 1
        for t in range(years):
            next = DataFrame({
                't': t,
                'VX Law': self.VX_law[t],
                'VDs': self.VDs[t] if t < self.PPP else 0,
                'VD PV': self.__VDPV(x, gender, i, t)
            }, index=[0])
            result = concat([result, next], ignore_index=True)
        self.result = result