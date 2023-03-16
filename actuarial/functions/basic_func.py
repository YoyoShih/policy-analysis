import math

''' Basic Annuity Functions '''
def a_imm_n(n, i=0.02):
    v = 1 / (1 + i)
    return (1 - v ** n) / i

def a_due_n(n, i=0.02):
    v = 1 / (1 + i)
    d = 1 - v
    return (1 - v ** n) / d

def a_bar_n(n, i=0.02):
    v = 1 / (1 + i)
    delta = math.log(1 + i)
    return (1 - v ** n) / delta

def a_imm_m_n(n, m, i=0.02):
    v = 1 / (1 + i)
    i_m = m * ((1 + i) ** (1 / m) - 1)
    return (1 - v ** n) / i_m

def a_due_m_n(n, m, i=0.02):
    v = 1 / (1 + i)
    d_m = m * (1 - v ** (1 / m))
    return (1 - v ** n) / d_m

''' Other Functions '''
def alpha(m, i=0.02):
    v = 1 / (1 + i)
    d = 1 - v
    i_m = m * ((1 + i) ** (1 / m) - 1)
    d_m = m * (1 - v ** (1 / m))
    return i * d / (i_m * d_m)

def beta(m, i=0.02):
    v = 1 / (1 + i)
    i_m = m * ((1 + i) ** (1 / m) - 1)
    d_m = m * (1 - v ** (1 / m))
    return (i - i_m) / (i_m * d_m)