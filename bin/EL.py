#%%
import pandas as pd
import xlwings as xw

#%% Basic parameters; Would not change
''' Product Specifications '''
sum_assured = 10000
PPP, pre_period = 20, 3
age_end, max_accepted_age = 105, 63
insurance_multiple = 1.025

''' Actuarial Assumptions '''
assumed_interest_rate = 0.02

''' File Settings '''
root_path = 'C:/Users/shih/ActuaViz/'
mortTable = pd.read_csv(f'{root_path}2021TSO.csv')
GPTable = pd.read_csv(f'{root_path}Insur Info/GP.csv')

''' Insured '''
gender = 0      # 0 = male, 1 = female
insured_age = 35

#%% Functions
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

#%% Excel Setting & Main
with xw.App(visible = True,add_book = False) as app:
    app.display_alerts = False 
    app.screen_updating = False

    try:
        wb = app.books.open('output.xlsx')
        try:
            sheet = wb.sheets('EL')
            sheet.clear()
        except:
            sheet = wb.sheets.add('EL')
    except:
        wb = app.books.add()
        sheet = wb.sheets[0]
        sheet.name = 'EL'
        
    sheet.range('A3:B5').value = [['年期', '性別'],
                            [PPP, gender],
                            ['年齡', 'EL']]
    for age in range(max_accepted_age):
        ''' Insurance Premium '''
        i = (GPTable["Gender"] == gender) & (GPTable["Age"] == age)
        annual_GP = GPTable[i]["GP"].tolist()[0]

        Bnf_PV = A(age, 0)
        NP = Bnf_PV / a(age, 0)
        EL = 1 - NP / annual_GP
        sheet.range(f'A{age + 6}:B{age + 6}').value = [age, EL]

    wb.save('output.xlsx') if wb.name == '活頁簿1' else wb.save()