import sys
sys.path.append("d:\\Desktop\\Actuarial Side Project\\Policy Analysis")
from actuarial.modules.KC1KC2 import pricing, reserve, valuation
import time

start = time.time()
# m = pricing.Pricing(35, 1, 0.02)
# print(m.DU)
# print(m.premium)
# print(m.alter)
# print(m.result)
# print(m.change_result)
# o = reserve.Reserve(35, 1)
# print(o.result)
# v = valuation.Valuation(35, 1, 0.026, 0.0319, 0.9, 1, 1, 0)
# print(v.result)
end = time.time()
print(format(end - start))