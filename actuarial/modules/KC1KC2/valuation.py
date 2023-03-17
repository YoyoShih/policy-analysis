from dataclasses import dataclass, field
from numpy import array, logspace, irr
from pandas import read_csv, DataFrame, concat
from actuarial.modules.KC1KC2.reserve import Reserve

''' Notation '''
# x: age
# ROI: return on investment # ROE: equity to asset ratio
# d_rate_m: discount rate for money # d_rate_p: discount rate for premium payment

''' File Settings '''
root_path = 'D:/Desktop/Actuarial Side Project/Policy Analysis/docs'
mortTable = read_csv(f'{root_path}/2021TSO.csv')
GPTable = read_csv(f'{root_path}/GP.csv')

assumptions = {
    'alpha per policy': 3471,
    'alpha percent of GP': 0.01802,
    'beta per policy': 376,
    'beta percent of GP': 0.00316,
    'gamma per policy': 0,
    'gamma percent of GP': 0.00924,
    'chia-tswan-dye per year': 0.0028,
    'chia-tswan-dye at least': 0.2,
    'chia-tswan-dye decline': 0.93,
    'business tax': 0.02,
    'override': 1.1,
    'commision rate': [0.32, 0.1, 0.05, 0.05, 0.05, 0.05],
    'default rate': [0.1, 0.08, 0.04, 0.03, 0.02, 0.015]
}

@dataclass
class Valuation:
    x: int
    gender: int
    ROI: float
    ROE: float
    death_rate: float
    default_rate: float
    expense_rate: float
    d_rate_p: float
    d_rate_m: float = field(init=False)   # by regulation
    reserve: Reserve = field(init=False)
    PPP: int = field(init=False)
    life: int = field(init=False)
    GP_tariff: int = field(init=False)
    GP_actual: int = field(init=False)
    insured_unit: int = field(init=False)

    def __post_init__(self):
        x, gender = self.x, self.gender
        self.d_rate_m = self.ROI
        self.insured_unit = 66
        main = Reserve(x, gender)
        pricing = main.pricing
        reserve = main.reserve
        self.__Result(main, pricing, reserve)
    
    def __Result(self, main, pricing, reserve):
        x, gender = self.x, self.gender
        insured_unit = self.insured_unit
        ROI, ROE, death_rate, default_rate, expense_rate, d_rate_p = self.ROI, self.ROE, self.death_rate, self.default_rate, self.expense_rate, self.d_rate_p
        d_rate_m = ROI
        PPP = reserve.PPP
        years = reserve.life
        alter_NPs = reserve.premium['alter NPs']
        override = assumptions['override']
        commision_rate = assumptions['commision rate']
        commision_len = len(commision_rate)
        m_result = main.result
        change_result = pricing.change_result
        r_result = reserve.result
        bnfs = r_result['A life']
        survival_annuity = reserve.survival_annuity
        S = reserve.S
        CVs = change_result['CV']
        VXs = m_result['VX Law']
        VDs = m_result['VD PV']
        index = (mortTable["Gender"] == gender) & (mortTable["Age"] >= x) & (mortTable["Age"] < x+years)
        mort_rates = mortTable[index]["MortRate"].to_numpy()
        initial_survival_rate = 1
        default_rates = assumptions['default rate'] + [assumptions['default rate'][-1]] * (years - 6)
        default_rates = [i * default_rate for i in default_rates]
        initial_asset = 0
        last_surplus = 0
        actuarial_VXs = r_result['VX']
        reserve_interest_rate = reserve.i
        last_actuarial_reserve = 0
        last_future_debt_law = 0
        ELR = pricing.premium['ELR']

        result = DataFrame(columns=[])
        for t in range(years):
            tariff_GP = reserve.premium['GP'] if t < PPP else 0
            actual_GP = tariff_GP * (1 - d_rate_p) if t < PPP else 0
            alter_NP = alter_NPs[t] if t < PPP else 0
            alpha = assumptions['alpha per policy'] / self.insured_unit + actual_GP * assumptions['alpha percent of GP'] if t == 0 else 0
            beta = assumptions['beta per policy'] / self.insured_unit + actual_GP * assumptions['beta percent of GP'] if t > 0 else 0
            gamma = assumptions['gamma per policy'] / self.insured_unit + actual_GP * assumptions['gamma percent of GP'] if t > 0 else 0
            commision_expense = actual_GP * commision_rate[t] * (1+override if t == 0 else 1) if t < commision_len else 0
            total_expense = (alpha + beta + gamma + commision_expense) * expense_rate
            bnf = bnfs[t]
            survival_expense = survival_annuity[t] + (S if t == years-1 else 0)
            CV = CVs[t]
            tax = max(actual_GP-alter_NP, 0) * assumptions['business tax']
            chia_tswan_dye = assumptions['chia-tswan-dye per year'] * (assumptions['chia-tswan-dye at least'] + (1 - assumptions['chia-tswan-dye at least']) * assumptions['chia-tswan-dye decline'] ** t)
            VX_reserve = VXs[t]
            VD_reserve = VDs[t]
            future_debt_law = VX_reserve + VD_reserve
            expected_mortality_rate = mort_rates[t]
            actual_mortality_rate = expected_mortality_rate * death_rate
            actuarial_default_rate = default_rates[t]
            middle_death_rate = initial_survival_rate * actual_mortality_rate
            end_default_rate = (initial_survival_rate - middle_death_rate) * actuarial_default_rate
            end_survival_rate = initial_survival_rate - middle_death_rate - end_default_rate
            actual_default_rate = end_default_rate / initial_survival_rate
            initial_premium_income = actual_GP * initial_survival_rate * insured_unit
            initial_expense = total_expense * initial_survival_rate * insured_unit
            middle_bnf_expense = bnf * middle_death_rate * insured_unit
            end_sur_expense = survival_expense * (end_default_rate + end_survival_rate) * insured_unit
            end_default_expense = CV * end_default_rate * insured_unit
            end_tax_expense = tax * initial_survival_rate * insured_unit
            end_ctd_expense =  chia_tswan_dye * VX_reserve * end_survival_rate * insured_unit
            end_interest_income = (initial_asset + initial_premium_income - initial_expense) * ROI - middle_bnf_expense * ((1 + ROI) ** 0.5 - 1)
            end_asset = initial_asset + initial_premium_income - initial_expense - middle_bnf_expense - end_sur_expense - end_default_expense - end_tax_expense - end_ctd_expense + end_interest_income
            end_debt = future_debt_law * end_survival_rate * insured_unit
            end_surplus = end_asset - end_debt
            net_income = end_surplus - last_surplus
            profit = end_surplus - last_surplus * (1 + ROI)
            break_even_year = t + 1 if end_surplus <= 0 else 0
            turnover_year = t + 1 if profit <= 0 else 0
            actuarial_reserve = actuarial_VXs[t] - survival_expense
            withdrawal_interest_rate = reserve_interest_rate
            withdrawal_mortality_rate = mort_rates[t]
            interest_surplus = ((alter_NP + last_actuarial_reserve) * (ROI - withdrawal_interest_rate) - bnf * withdrawal_mortality_rate * ((1 + ROI) ** 0.5 - (1 + withdrawal_interest_rate) ** 0.5)) * initial_survival_rate * insured_unit
            death_surplus = (actuarial_reserve + survival_expense - bnf * (1 + withdrawal_interest_rate) ** 0.5) * (actual_mortality_rate - withdrawal_mortality_rate) * initial_survival_rate * insured_unit
            expense_surplus = ((actual_GP - total_expense - alter_NP) * (1 + withdrawal_interest_rate) - tax) * initial_survival_rate * insured_unit
            default_surplus = actual_default_rate * (actuarial_reserve - CV) * initial_survival_rate * insured_unit
            debt_margin = ((last_future_debt_law - last_actuarial_reserve) * (1 + withdrawal_interest_rate) - (1 - withdrawal_mortality_rate) * (future_debt_law - actuarial_reserve)) * initial_survival_rate * insured_unit
            interestXdeath = -bnf * (actual_mortality_rate - withdrawal_mortality_rate) * ((1 + ROI) ** 0.5 - (1 + withdrawal_interest_rate) ** 0.5) * initial_survival_rate * insured_unit
            interestXexpense = (actual_GP - alter_NP - total_expense) * (ROI - withdrawal_interest_rate) * initial_survival_rate * insured_unit
            interestXdebt = (last_future_debt_law - last_actuarial_reserve) * (ROI - withdrawal_interest_rate) * initial_survival_rate * insured_unit
            defaultXdebt = actual_default_rate * (future_debt_law - actuarial_reserve) * initial_survival_rate * insured_unit
            deathXdebt = (actual_mortality_rate - withdrawal_mortality_rate) * (future_debt_law - actuarial_reserve) * initial_survival_rate * insured_unit
            ctd_interact_factor = -(1 - actual_mortality_rate - actual_default_rate) * chia_tswan_dye * future_debt_law * initial_survival_rate * insured_unit
            EL = tariff_GP * ELR
            fix_cost = (assumptions['beta per policy'] + assumptions['gamma per policy']) / insured_unit if t > 0 else assumptions['alpha per policy'] / insured_unit
            variable_cost = actual_GP * assumptions['alpha percent of GP'] if t == 0 else actual_GP * (assumptions['beta percent of GP'] + assumptions['gamma percent of GP'])
            commision_cost = commision_expense
            initial_EL_income = EL * initial_survival_rate * insured_unit
            initial_fix_cost = fix_cost * initial_survival_rate * insured_unit
            initial_variable_cost = variable_cost * initial_survival_rate * insured_unit
            initial_commision_cost = commision_cost * initial_survival_rate * insured_unit
            end_tax_cost = end_tax_expense
            end_ctd_cost = end_ctd_expense
            next = DataFrame({
                't': t+1,
                'x': x+t,
                'tariff GP': tariff_GP,
                'actual GP': actual_GP,
                'alter NPs': alter_NP,
                'alpha': alpha,
                'beta': beta,
                'gamma': gamma,
                'commision expense': commision_expense,
                'total expense': total_expense,
                'benefit in year': bnf,
                'survival expense': survival_expense,
                'CV': CV,
                'tax': tax,
                'chia-tswan-dye': chia_tswan_dye,
                'VX reserve': VX_reserve,
                'VD reserve': VD_reserve,
                'future debt in law': future_debt_law,
                'rate of return on investment': ROI,
                'expected mortality rate': expected_mortality_rate,
                'actual mortality rate': actual_mortality_rate,
                'actual default rate': actual_default_rate,
                'actuarial default rate': actuarial_default_rate,
                'initial survival rate': initial_survival_rate,
                'middle death rate': middle_death_rate,
                'end default rate': end_default_rate,
                'end survival rate': end_survival_rate,
                'initial asset': initial_asset,
                'initial premium income': initial_premium_income,
                'initial expense': initial_expense,
                'middle benefit expense': middle_bnf_expense,
                'end survival expense': end_sur_expense,
                'end default expense': end_default_expense,
                'end tax expense': end_tax_expense,
                'end chia-tswan-dye expense': end_ctd_expense,
                'end interest income': end_interest_income,
                'end asset': end_asset,
                'end debt': end_debt,
                'end surplus': end_surplus,
                'net income': net_income,
                'profit': profit,
                'break-even year': break_even_year,
                'turnover year': turnover_year,
                'actuarial reserve': actuarial_reserve,
                'withdrawal interest rate': withdrawal_interest_rate,
                'withdrawal mortality rate': withdrawal_mortality_rate,
                'interest surplus': interest_surplus,
                'death surplus': death_surplus,
                'expense surplus': expense_surplus,
                'default surplus': default_surplus,
                'debt margin': debt_margin,
                'interest x death': interestXdeath,
                'interest x expense': interestXexpense,
                'interest x debt': interestXdebt,
                'default x debt': defaultXdebt,
                'death x debt': deathXdebt,
                'ctd interact factor': ctd_interact_factor,
                'expense loading': EL,
                'fix cost': fix_cost,
                'variable cost': variable_cost,
                'commision cost': commision_expense,
                'initial EL income': initial_EL_income,
                'initial fix cost': initial_fix_cost,
                'initial variable cost': initial_variable_cost,
                'initial commision cost': initial_commision_cost,
                'end tax cost': end_tax_cost,
                'end ctd cost': end_ctd_cost
            }, index=[0])
            result = concat([result, next], ignore_index=True)
            initial_survival_rate = end_survival_rate
            last_surplus = end_surplus
            last_actuarial_reserve = actuarial_reserve
            last_future_debt_law = future_debt_law
        self.result = result

        NPVfunc = self.NPV
        premium_PV = NPVfunc(d_rate_m, result['initial premium income']) * (1 + d_rate_m)
        profit_PV1 = NPVfunc(d_rate_m, result['profit'])
        profit_PV2 = NPVfunc(ROE, result['profit'])
        interest_surplus_PV = NPVfunc(d_rate_m, result['interest surplus'])
        death_surplus_PV = NPVfunc(d_rate_m, result['death surplus'])
        expense_surplus_PV = NPVfunc(d_rate_m, result['expense surplus'])
        default_surplus_PV = NPVfunc(d_rate_m, result['default surplus'])
        debt_margin_PV = NPVfunc(d_rate_m, result['debt margin'])
        interestXdeath_PV = NPVfunc(d_rate_m, result['interest x death'])
        interestXexpense_PV = NPVfunc(d_rate_m, result['interest x expense'])
        interestXdebt_PV = NPVfunc(d_rate_m, result['interest x debt'])
        defaultXdebt_PV = NPVfunc(d_rate_m, result['default x debt'])
        deathXdebt_PV = NPVfunc(d_rate_m, result['death x debt'])
        ctd_interact_factor_PV = NPVfunc(d_rate_m, result['ctd interact factor'])
        self.PVs = {
            'premium': premium_PV,
            'profit using discount rate': profit_PV1,
            'profit using ROE': profit_PV2,
            'profit source': {
                'interest surplus': interest_surplus_PV,
                'death surplus': death_surplus_PV,
                'expense surplus': expense_surplus_PV,
                'default surplus': default_surplus_PV,
                'debt margin': debt_margin_PV,
                'interest x death': interestXdeath_PV,
                'interest x expense': interestXexpense_PV,
                'interest x debt': interestXdebt_PV,
                'default x debt': defaultXdebt_PV,
                'death x debt': deathXdebt_PV,
                'ctd interact factor': ctd_interact_factor_PV
            }
        }

        c_reserve = (VXs[0] + survival_annuity[0]) / actual_GP
        c_premium_insufficient = VDs[0] / actual_GP
        c_fix = assumptions['alpha per policy'] / (actual_GP * insured_unit)
        c_variable = assumptions['alpha percent of GP'] * tariff_GP / actual_GP
        c_commision = assumptions['commision rate'][0] * (1 + assumptions['override'])
        self.summarize = {
            'cost assessment': {
                'reserve': c_reserve,
                'premium insufficient': c_premium_insufficient,
                'fix': c_fix,
                'variable': c_variable,
                'commision': c_commision,
                'initial total': c_reserve + c_premium_insufficient + c_fix + c_variable + c_commision
            },
            'profit source analysis': {
                'profit': profit_PV1 / premium_PV,
                'interest surplus': (interest_surplus_PV + interestXdebt_PV) / premium_PV,
                'death surplus': (death_surplus_PV + interestXdeath_PV + deathXdebt_PV) / premium_PV,
                'expense surplus': (expense_surplus_PV + debt_margin_PV + interestXexpense_PV + ctd_interact_factor_PV) / premium_PV,
                'default surplus': (default_surplus_PV + defaultXdebt_PV) / premium_PV
            },
            'profit index': {
                'PV of net income / initial premium': profit_PV2 / (actual_GP * insured_unit),
                'AV of net income': profit_PV1 * (1 + d_rate_m) ** years,
                'break-even': max(result['break-even year']) + 1,
                'turnover': max(result['turnover year']) + 1,
                'IRR': irr(result['profit'])
            }
        }
    
    def NPV(self, rate, values):
        years = len(values)
        values_array = array(values)
        discounts_array = logspace(-1, -years, num=years, base=1+rate)
        return sum(values_array*discounts_array)