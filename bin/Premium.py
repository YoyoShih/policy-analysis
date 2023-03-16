import numpy as np
import pandas as pd
import xlwings as xw

# Basic parameters; Would not change
''' Product Specifications '''
sum_assured = 10000
PPP, pre_period, sur_period = 20, 3, 15
age_end = 105
insurance_multiple = 1.025

''' Actuarial Assumptions '''
assumed_interest_rate = 0.02

''' File Settings '''
root_path = 'C:/Users/shih/ActuaViz/docs/'
mortTable = pd.read_csv(f'{root_path}2021TSO.csv')
GPTable = pd.read_csv(f'{root_path}Insur Info/GP.csv')

''' Insured '''
gender = 0      # 0 = male, 1 = female
insured_age = 35

''' Insurance Premium '''
i = (GPTable["Gender"] == gender) & (GPTable["Age"] == insured_age)
annual_GP = GPTable[i]["GP"].tolist()[0]

# Functions
def a(age, t):
    ''' The Probability of Survival in the Beginning of Period '''
    survivals = 1
    
    ''' Initial Settings '''
    a = 0
    
    for year in range(PPP - t):
        ''' Mortality Rate '''
        i = (mortTable["Gender"] == gender) & (mortTable["Age"] == age + year)
        mort_rate = mortTable[i]["MortRate"].tolist()[0]
        deaths = survivals * mort_rate
        
        ''' Calculate a '''
        a += survivals * (1 + assumed_interest_rate) ** (-year)
        
        ''' The Probability of Survival in the End of Period '''
        survivals -= deaths
    return a

def A(age, t):
    ''' The Probability of Survival in the Beginning of Period '''
    survivals = 1
    
    ''' Initial Settings '''
    A = 0
    discount = (1 + assumed_interest_rate) ** -0.5
    
    for year in range(age_end - age):
        ''' Mortality Rate '''
        i = (mortTable["Gender"] == gender) & (mortTable["Age"] == age + year)
        mort_rate = mortTable[i]["MortRate"].tolist()[0]
        deaths = survivals * mort_rate
        
        ''' Insurance Benefit Cost '''
        if year < pre_period - t:
            A += annual_GP * (year + t + 1) * insurance_multiple * deaths * discount
        else:
            A += sum_assured * deaths * discount
        
        ''' The Probability of Survival in the End of Period '''
        survivals -= deaths
        discount /= (1 + assumed_interest_rate)
    
    ''' Age End Benefit '''
    A += sum_assured * survivals * (1 + assumed_interest_rate) ** (-(age_end - age))
    return A

# Excel Setting & Main
with xw.App(visible = True, add_book = False) as app:
    app.display_alerts = False 
    app.screen_updating = False

    try:
        wb = app.books.open('output.xlsx')
        try:
            sheet = wb.sheets('Pricing')
            sheet.clear()
        except:
            sheet = wb.sheets.add('Pricing')
    except:
        wb = app.books.add()
        sheet = wb.sheets[0]
        sheet.name = 'Pricing'

    sheet.range('A3:B7').value = np.transpose(np.array([
        ['性別', '年齡', '年期', '保障', '保額'],
        [gender, insured_age, PPP, age_end - insured_age, sum_assured]
        ]))

    cols = ['t', 'x', 'q', 'L', 'Bnf', 'Bnf PV', 'NP', 'NP PV', 'VL', 'Surrender Value']
    sheet.range('D1:M1').value = cols

    L = 1

    for t in range(age_end - insured_age + 1):
        x = insured_age + t
        i = (mortTable["Gender"] == gender) & (mortTable["Age"] == x)
        q = mortTable[i]["MortRate"].tolist()[0] if t == age_end - insured_age else 0
        d = L * q
        Bnf = annual_GP * (t + 1) * insurance_multiple if t < pre_period else sum_assured
        Bnf_PV = A(x, t)
        if t == 0:
            NP = Bnf_PV / a(x, t)
            EL = 1 - NP / annual_GP
        NP_PV = NP * a(x, t)
        VL = Bnf_PV - NP_PV
        SV = VL * (0.75 + 0.25 * (t + 1) / sur_period) if t < sur_period else VL
        sheet.range(f'D{t + 2}:M{t + 2}').value = [t, x, q, L, Bnf, Bnf_PV, NP, NP_PV, VL, SV]
        L -= d
    
    wb.save('output.xlsx') if wb.name == '活頁簿1' else wb.save()