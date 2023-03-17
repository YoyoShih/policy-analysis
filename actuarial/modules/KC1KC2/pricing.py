from dataclasses import dataclass, field
from pandas import read_csv, DataFrame, concat
from numpy import arange, array, logspace, full, concatenate, cumsum, ndarray, where, zeros
from actuarial.functions.Annuity import a_due_x_n
from actuarial.functions.Benefit import A_bar_x, nEx

''' Notation '''
# x: age    # omega: age end    # i: interest rate  # S: sum assured    PPP: Premiums Payment Period   
# multiple: benefit multiple in preperiod   # pre-period: period that benefit equal premium * multiple

# purpose: 0 -> pricing, 1 -> reserve

''' File Settings '''
root_path = 'D:/Desktop/Actuarial Side Project\Policy Analysis\docs'
mortTable = None    # mortTable!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
GPTable = read_csv(f'{root_path}Insur Info/GP.csv')

@dataclass
class Pricing:
    x: int
    gender: int
    i: float = 0.02
    purpose: int = 0
    S: int = 10000
    PPP: int = 20
    pre_period: int = 3
    omega: int = 105
    multiple: float = 1.025
    DU: float = field(init=False)
    life: int = field(init=False)
    premiums: dict = field(init=False)
    survival_annuity: ndarray = field(init=False)
    alter: dict = field(init=False)
    result: DataFrame = field(init=False)

    def __post_init__(self):
        x, gender, i, purpose = self.x, self.gender, self.i, self.purpose
        self.life = self.omega - self.x
        self.survival_annuity = zeros(self.life)
        index = (GPTable["Gender"] == gender) & (GPTable["Age"] == x)
        self.premium = {
            'GP': GPTable[index]["GP"].tolist()[0]
        }
        self.__Premiums(x, gender, i)
        self.alter = {}
        self.__AlterNP(x, gender, i)
        self.__DU(x, gender, i)
        self.__Result(x, gender, i, purpose)
        if purpose == 0:
            self.__Change(x, gender, i)
    
    ''' Whole Life Benefit A Funcs '''
    def __A_x_bnf(self, x, gender, i, t=0):
        S, pre_period, multiple = self.S, self.pre_period, self.multiple
        GP = self.premium['GP']
        years = self.life
        discounts = logspace(-0.5, -(years-t-0.5), num=years-t, base=1+i)
        BNFs1 = arange(start=GP, stop=GP*pre_period+1, step=GP) * multiple
        BNFs2 = full(years-max(t, pre_period), S)
        BNFs = concatenate((BNFs1[t:], BNFs2))
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] >= x+t) & (mortTable["Age"] < x+years)
        mort_rates = mortTable[index]["MortRate"].to_numpy()
        survivals_rate = concatenate(([1], (lambda x: 1-x)(mort_rates)[:-1]))
        survivals = survivals_rate.cumprod()
        return sum(discounts*BNFs*survivals*mort_rates)
    
    ''' Whole Life Benefit A Funcs '''
    def __A_x_sa(self, x, gender, i, t=0):
        sa = self.survival_annuity[t:]
        years = self.life
        discounts = logspace(-0.5, -(years-t-0.5), num=years-t, base=1+i)
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] >= x+t) & (mortTable["Age"] < x+years)
        mort_rates = mortTable[index]["MortRate"].to_numpy()
        survivals_rate = concatenate(([1], (lambda x: 1-x)(mort_rates)[:-1]))
        survivals = survivals_rate.cumprod()
        return sum(discounts*sa*survivals*mort_rates)

    ''' Term A Funcs '''
    def __A_n_x(self, x, gender, i, t):
        S, pre_period, multiple = self.S, self.pre_period, self.multiple
        GP = self.premium['GP']
        years = self.life - t
        discounts = logspace(-0.5, -(years-0.5), num=years, base=1+i)
        BNFs1 = arange(start=GP, stop=GP*pre_period+1, step=GP) * multiple
        BNFs2 = full(years+t-pre_period, S)
        BNFs = concatenate((BNFs1, BNFs2))[t:t+years]
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] >= x+t) & (mortTable["Age"] < x+years+t)
        mort_rates = mortTable[index]["MortRate"].to_numpy()
        survivals_rate = concatenate(([1], (lambda x: 1-x)(mort_rates)[:-1]))
        survivals = survivals_rate.cumprod()
        return cumsum(discounts*BNFs*survivals*mort_rates)

    ''' Whole Life a Funcs '''
    def __a_due_x(self, x, gender, i):
        PPP, life = self.PPP, self.life
        years = min(life, PPP)
        discounts = logspace(0, -(years-1), num=years, base=1+i)
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] >= x) & (mortTable["Age"] < x+years)
        mort_rates = mortTable[index]["MortRate"].to_numpy()
        survivals_rate = concatenate(([1], (lambda x: 1-x)(mort_rates)[:-1]))
        survivals = survivals_rate.cumprod()
        return sum(discounts*survivals)
  
    ''' Premiums Funcs '''
    def __Premiums(self, x, gender, i):
        S, omega = self.S, self.omega
        NP_life = (self.__A_x_bnf(x, gender, i) + S * nEx(x, gender, omega, omega, i)) / self.__a_due_x(x, gender, i)
        self.premium['NP_life'] = NP_life
    
    ''' Alter NP '''
    def __AlterNP(self, x, gender, i):
        PPP, omega, multiple = self.PPP, self.omega, self.multiple
        NP_sur = self.__A_x_sa(x, gender, i) / self.__a_due_x(x, gender, i)
        NP_life, GP = self.premium['NP_life'], self.premium['GP']
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] == x)
        mort_rate = mortTable[index]["MortRate"].tolist()[0]
        PF = GP * multiple * mort_rate * (1 + i) ** -0.5
        h = self.__A_x_bnf(x, gender, i) / (A_bar_x(x, gender, omega, i, method=1) * 10000)
        P20 = A_bar_x(x, gender, 110, i, method=1) * 10000 / a_due_x_n(x, gender, 20, 110, i)
        Modify = 20 if NP_life > h * P20 else 1
        m = PPP if Modify == 1 else min(20, PPP)
        P1 = (PF if Modify == 1 else PF + max(0, NP_life-h*P20)) + NP_sur
        P2 = (NP_life + (NP_life - P1) / (a_due_x_n(x, gender, m, omega, i) - 1)) + NP_sur
        P3 = (NP_life if PPP > Modify else 0) + NP_sur
        alter_NPs = []
        append = alter_NPs.append
        for t in range(PPP):
            alter_NP = (P2 if 0 < t < Modify \
                else (P3 if t >= Modify \
                    else P1))
            append(alter_NP)
        self.alter = {
            'NP_life': NP_life,
            'NP_sur': NP_sur,
            'PF': PF,
            'h': h,
            'P20': P20,
            'Modify': Modify,
            'P1': P1,
            'P2': P2,
            'P3': P3
        }
        NP = NP_life + NP_sur
        self.premium['NP'] = NP
        self.premium['ELR'] = 1 - NP / GP
        self.premium['alter NPs'] = alter_NPs

    def __AlterNPPV(self, x, gender, i, t=0):
        PPP, life = self.PPP, self.life
        alter_NPs = array(self.premium['alter NPs'][t:])
        years = max(0, min(life, PPP)-t)
        discounts = logspace(0, -(years-1), num=years, base=1+i)
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] >= x+t) & (mortTable["Age"] < x+min(PPP, life))
        mort_rates = mortTable[index]["MortRate"].to_numpy()
        survivals_rate = concatenate(([1], (lambda x: 1-x)(mort_rates)[:-1]))
        survivals = survivals_rate.cumprod()
        return sum(alter_NPs*survivals*discounts)

    ''' DU calculation '''
    def __A_x_bnf_t(self, x, gender, i):
        S, pre_period, multiple = self.S, self.pre_period, self.multiple
        GP = self.premium['GP']
        years = self.life
        discounts = logspace(-0.5, -(years-0.5), num=years, base=1+i)
        ts = arange(start=0.5, stop=years+0.5, step=1)
        BNFs1 = arange(start=GP, stop=GP*pre_period+1, step=GP) * multiple
        BNFs2 = full(years-pre_period, S)
        BNFs = concatenate((BNFs1, BNFs2))
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] >= x) & (mortTable["Age"] < x+years)
        mort_rates = mortTable[index]["MortRate"].to_numpy()
        survivals_rate = concatenate(([1], (lambda x: 1-x)(mort_rates)[:-1]))
        survivals = survivals_rate.cumprod()
        return sum(discounts*ts*BNFs*survivals*mort_rates)
    
    def __A_x_sa_t(self, x, gender, i, t=0):
        sa = self.survival_annuity[t:]
        years = self.life
        discounts = logspace(-0.5, -(years-t-0.5), num=years-t, base=1+i)
        ts = arange(start=0, stop=years, step=1)
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] >= x+t) & (mortTable["Age"] < x+years)
        mort_rates = mortTable[index]["MortRate"].to_numpy()
        survivals_rate = concatenate(([1], (lambda x: 1-x)(mort_rates)[:-1]))
        survivals = survivals_rate.cumprod()
        return sum(discounts*ts*sa*survivals*mort_rates)

    def __DU(self, x, gender, i):
        S, omega = self.S, self.omega
        bnf = self.__A_x_bnf(x, gender, i)
        end = S * nEx(x, gender, omega, omega, i)
        sur = self.__A_x_sa(x, gender, i)
        bnf_t = self.__A_x_bnf_t(x, gender, i)
        end_t = self.life * S * nEx(x, gender, omega, omega, i)
        sur_t = self.__A_x_sa_t(x, gender, i)
        self.DU = (bnf_t + end_t + sur_t) / (bnf + end + sur)

    ''' Search the position of one-time premium '''
    def __search_A_n_x(self, x, gender, i, t, one_time_premium):
        extends = self.__A_n_x(x, gender, i, t)
        year = sum(where(extends <= one_time_premium, 1, 0))
        day = 365*(one_time_premium-extends[year-1])/(extends[year]-extends[year-1]) if 0 < year < 69 else 0
        return year, day

    ''' Result '''
    def __Result(self, x, gender, i, purpose):
        S, PPP, omega = self.S, self.PPP, self.omega
        alter_NPs = self.premium['alter NPs']
        last_col = 'VL' if purpose == 0 else 'VX'
        cols = ['t', 'x', 'A life', 'A survival', 'alter NP', 'alter NP PV', last_col]
        result = DataFrame(columns=cols)
        years = self.life
        self_A_x_bnf = self.__A_x_bnf
        self_A_x_sur = self.__A_x_sa
        self_AlterNPPV = self.__AlterNPPV
        for t in range(years + 1):
            A_x_life = self_A_x_bnf(x, gender, i, t) + S * nEx(x, gender, omega, omega, i, t)
            A_x_sur = self_A_x_sur(x, gender, i, t)
            alter_NP_PV = self_AlterNPPV(x, gender, i, t)
            next = DataFrame({
                't': t,
                'x': x + t,
                'A life': A_x_life,
                'A surival': A_x_sur,
                'alter NP': alter_NPs[t] if t < PPP else 0,
                'alter NP PV': alter_NP_PV,
                last_col: A_x_life + A_x_sur - alter_NP_PV
            }, index=[0])
            result = concat([result, next], ignore_index=True)
        self.result = result

    def __Change(self, x, gender, i):
        S, PPP, omega = self.S, self.PPP, self.omega
        VL = self.result['VL']
        sur = self.survival_annuity
        cols = ['t', 'x', 'VL', 'CV', 'SC', 'One-time Premium', 'PV', 'Sum Assured After', 'Ex Year', 'Ex Day']
        change_result = DataFrame(columns=cols)
        years = self.life
        self_A_x_bnf = self.__A_x_bnf
        self_A_x_sur = self.__A_x_sa
        self_search_A_n_x = self.__search_A_n_x
        for t in range(years):
            A_x_life = self_A_x_bnf(x, gender, i, t) + S * nEx(x, gender, omega, omega, i, t)
            A_x_sur = self_A_x_sur(x, gender, i, t)
            A_x = A_x_life + A_x_sur - sur[t]
            VLt = VL[t]
            CV = VLt * (0.75 + 0.25 * min(t, 15) / min(PPP, 15))    # do not include survival annuity
            SC = min(S*0.01, VLt-CV)
            one_time_premium = VLt - SC if 0 < t < PPP else 0    # do not include survival annuity
            ex_year, ex_day = self_search_A_n_x(x, gender, i , t, one_time_premium)
            next = DataFrame({
                't': t,
                'x': x + t,
                'VL': VLt,
                'CV': CV,
                'SC': SC,
                'One-time Premium': one_time_premium,
                'PV': A_x,
                'Sum Assured After': one_time_premium * S / A_x if 0 < t < PPP else 0,
                'Ex Year': ex_year+t if 0 < t < PPP else 0,
                'Ex Day': ex_day if 0 < t < PPP else 0
            }, index=[0])
            change_result = concat([change_result, next], ignore_index=True)
        self.change_result = change_result